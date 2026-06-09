from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Installation
from .forms import InstallationForm
import json
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from django.core.paginator import Paginator
from django.db.models import Q

# =========================
# INSTALLATION LIST (PAGINATION)
# =========================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])


def installation_list(request):
    search = request.GET.get('search', '')

    entries = Installation.objects.all()

    if search:
        entries = entries.filter(
            Q(ms_id__icontains=search)
        )

    paginator = Paginator(entries, 50)
    page_number = request.GET.get('page')
    entries = paginator.get_page(page_number)

    return render(
        request,
        'installation/installation_list.html',
        {
            'entries': entries,
            'search': search,
        }
    )
# =========================
# ADD
# =========================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def add_installation(request):

    form = InstallationForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('installation_list')

    return render(request, 'installation/installation_form.html', {
        'form': form
    })


# =========================
# EDIT
# =========================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def edit_installation(request, pk):

    obj = get_object_or_404(Installation, pk=pk)

    form = InstallationForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect('installation_list')

    return render(request, 'installation/installation_form.html', {
        'form': form
    })


# =========================
# DELETE
# =========================
@login_required
@role_required(['admin'])
def delete_installation(request, pk):

    obj = get_object_or_404(Installation, pk=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('installation_list')

    return render(request, 'installation/delete_confirm.html', {
        'entry': obj
    })


# =========================
# INLINE UPDATE (AJAX SAFE)
# =========================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def update_entry(request, pk):

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            field = data.get("field")
            value = data.get("value")

            obj = get_object_or_404(Installation, pk=pk)

            allowed_fields = [
                "status",
                "abd_number",
                "start_date",
                "end_date"
            ]

            if field not in allowed_fields:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid field"
                })

            # handle empty dates safely
            if field in ["start_date", "end_date"] and not value:
                value = None

            setattr(obj, field, value)
            obj.save()

            return JsonResponse({
                "success": True,
                "field": field,
                "value": value
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

    return JsonResponse({
        "success": False,
        "error": "Invalid request"
    })


# =========================
# F2 TB PAGE (SEARCH BY ms_id_full)
# =========================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def f2_tb(request):

    ms_id_full = request.GET.get("ms_id_full", "").strip()

    entries = []
    message = None

    if ms_id_full:

        entries = Installation.objects.filter(
            ms_id_full__icontains=ms_id_full
        ).order_by('-id')

        if entries.exists():
            message = f"{entries.count()} record(s) found"
        else:
            message = "No data found"

    return render(request, "installation/f2_tb.html", {

        "ms_id_full": ms_id_full,
        "entries": entries,
        "message": message

    })


# =========================
# F2 TB SAVE (UPDATE UNIQUE ROW ONLY)
# =========================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def f2_tb_save(request):

    if request.method == "POST":

        data = json.loads(request.body)

        obj = Installation.objects.filter(
            id=data.get("id")
        ).first()

        if not obj:

            return JsonResponse({
                "success": False,
                "message": "Record not found"
            })

        # ================= UPDATE ONLY THIS UNIQUE ROW =================
        obj.status = data.get("status")

        obj.abd_number = data.get("abd_number")

        obj.start_date = (
            data.get("start_date") or None
        )

        obj.end_date = (
            data.get("end_date") or None
        )

        obj.save()

        return JsonResponse({

            "success": True,
            "message": f"{obj.ms_id_full} updated successfully"

        })

    return JsonResponse({
        "success": False,
        "message": "Invalid request"
    })
    # =========================
# OPTIONAL AJAX SEARCH API
# =========================
# =========================
# OPTIONAL AJAX SEARCH API
# =========================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def f2_tb_search(request):

    ms_id_full = request.GET.get(
        "ms_id_full",
        ""
    ).strip()

    if not ms_id_full:

        return JsonResponse({
            "results": []
        })

    qs = Installation.objects.filter(

        ms_id_full__icontains=ms_id_full

    ).order_by('-id')

    results = []

    for i in qs:

        results.append({

            "id": i.id,

            "ms_id_full": i.ms_id_full,

            "ms_id": i.ms_id,

            "status": i.status,

            "abd_number": i.abd_number,

            "start_date": (
                str(i.start_date)
                if i.start_date else ""
            ),

            "end_date": (
                str(i.end_date)
                if i.end_date else ""
            ),

            "system": i.system,

            "facility": i.facility,

            "stage": i.stage,

        })

    return JsonResponse({
        "results": results
    })
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import ExtractYear
from .models import Installation

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def dashboard(request):

    qs = Installation.objects.all()

    # =========================
    # TOTAL COUNTS (UNIQUE)
    # =========================
    total_facility = qs.values('facility').distinct().count()
    total_system = qs.values('system').distinct().count()
    total_ms_id = qs.values('ms_id').distinct().count()
    total_saw_program = qs.values('saw_program').distinct().count()

    # =========================
    # STATUS PIE CHART
    # =========================
    status_qs = qs.values('status').annotate(total=Count('id'))

    status_labels = [i['status'] for i in status_qs]
    status_values = [i['total'] for i in status_qs]

    # =========================
    # YEARLY COMPLETED (END DATE)
    # =========================
    yearly_qs = (
        qs.filter(status="Completed", end_date__isnull=False)
        .annotate(year=ExtractYear('end_date'))
        .values('year')
        .annotate(total=Count('id'))
        .order_by('year')
    )

    year_labels = [str(i['year']) for i in yearly_qs]
    year_values = [i['total'] for i in yearly_qs]

    return render(request, "installation/dashboard.html", {
        "total_facility": total_facility,
        "total_system": total_system,
        "total_ms_id": total_ms_id,
        "total_saw_program": total_saw_program,

        "status_labels": json.dumps(status_labels),
        "status_values": json.dumps(status_values),

        "year_labels": json.dumps(year_labels),
        "year_values": json.dumps(year_values),
    })

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def dashboard_filter(request):

    filter_type = request.GET.get('type')
    chart = request.GET.get('chart')
    value = request.GET.get('value')

    title = ""
    records = []

    # CARD CLICK
    if filter_type == "facility":

        title = "Facility List"

        qs = (
            Installation.objects
            .values('facility')
            .distinct()
            .order_by('facility')
        )

        records = [{'name': r['facility']} for r in qs]

    elif filter_type == "system":

        title = "System List"

        qs = (
            Installation.objects
            .values('system')
            .distinct()
            .order_by('system')
        )

        records = [{'name': r['system']} for r in qs]

    elif filter_type == "ms":

        title = "Milestone List"

        qs = (
            Installation.objects
            .values('ms_id')
            .distinct()
            .order_by('ms_id')
        )

        records = [{'name': r['ms_id']} for r in qs]

    elif filter_type == "saw":

        title = "SAW Program List"

        qs = (
            Installation.objects
            .values('saw_program')
            .distinct()
            .order_by('saw_program')
        )

        records = [{'name': r['saw_program']} for r in qs]

    # PIE CHART CLICK
    if chart == "status":

        title = f"Status : {value}"

        records = (
            Installation.objects
            .filter(status=value)
            .values(
                'facility',
                'system',
                'ms_id',
                'status'
            )
            .order_by('facility')
        )

    # BAR CHART CLICK
    elif chart == "year":

        title = f"Completed Year : {value}"

        records = (
            Installation.objects
            .filter(
                status="Completed",
                end_date__year=value
            )
            .values(
                'facility',
                'system',
                'ms_id',
                'end_date'
            )
            .order_by('end_date')
        )

    context = {
        'title': title,
        'records': records
    }

    return render(request, 'installation/filter_page.html', context)



# views.py

from collections import defaultdict
from django.shortcuts import render
from .models import Installation

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def facility_dashboard(request):

    data = Installation.objects.all().order_by('facility', 'system')

    facility_data = defaultdict(list)

    for item in data:

        # color logic
        if item.status.lower() == "completed":
            color = "success"   # green
        else:
            color = "primary"   # blue

        facility_data[item.facility].append({
            'system': item.system,
            'status': item.status,
            'color': color,
            'ms_id': item.ms_id,
            'abd_number': item.abd_number,
        })

    context = {
        'facility_data': dict(facility_data)
    }

    return render(request, 'installation/facility_dashboard.html', context)


from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import P4IDForm
from .models import P4ID, Installation

# ================= CREATE =================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p4_create(request):

    if request.method == 'POST':

        form = P4IDForm(request.POST)

        if form.is_valid():

            p4 = form.save()

            ms_id = request.POST.get('ms_ids', '').strip()

            installation = Installation.objects.filter(
                ms_id=ms_id
            ).first()

            if installation:
                p4.ms_ids.set([installation])
            else:
                p4.ms_ids.clear()

            return redirect('p4_display_list')

    else:
        form = P4IDForm()

    return render(request,
                  'installation/p4_entry.html',
                  {
                      'form': form,
                      'selected_ms_id': '',
                      'selected_ms_label': '',
                  })
# ================= DISPLAY =================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p4_list(request):

    data = P4ID.objects.prefetch_related(
        'ms_ids'
    ).order_by('-id')

    return render(request,
                  'installation/p4_display_list.html',
                  {
                      'data': data
                  })


# ================= SEARCH =================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def search_ms(request):

    q = request.GET.get('q', '').strip()

    results = Installation.objects.filter(
        ms_id__icontains=q
    )[:10]

    data = [
        {
            "id": item.id,
            "ms_id": item.ms_id,
            "system": item.system
        }
        for item in results
    ]

    return JsonResponse(data, safe=False)



# ================= EDIT =================
# ================= EDIT =================
# ================= EDIT =================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p4_edit(request, id):

    p4 = get_object_or_404(P4ID, id=id)

    if request.method == 'POST':

        form = P4IDForm(request.POST, instance=p4)

        if form.is_valid():

            p4 = form.save()

            ms_id = request.POST.get('ms_ids', '').strip()

            installation = Installation.objects.filter(
                ms_id=ms_id
            ).first()

            if installation:
                p4.ms_ids.set([installation])
            else:
                p4.ms_ids.clear()

            return redirect('p4_display_list')

    else:
        form = P4IDForm(instance=p4)

    selected_installation = p4.ms_ids.first()

    selected_ms_id = ''
    selected_ms_label = ''

    if selected_installation:
        selected_ms_id = selected_installation.ms_id
        selected_ms_label = (
            f'{selected_installation.ms_id} || '
            f'{selected_installation.system}'
        )

    return render(request,
                  'installation/p4_entry.html',
                  {
                      'form': form,
                      'selected_ms_id': selected_ms_id,
                      'selected_ms_label': selected_ms_label,
                  })# ================= DELETE =================
@login_required
@role_required(['admin'])
def p4_delete(request, id):

    p4 = get_object_or_404(P4ID, id=id)

    p4.delete()

    return redirect('p4_display_list')


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .forms import P8IDForm
from .models import P8ID, P4ID

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
# ================= CREATE =================
def p8_create(request):

    if request.method == 'POST':

        form = P8IDForm(request.POST)

        if form.is_valid():

            p8 = form.save()

            # selected p4 ids
            p4_ids = request.POST.get('p4_ids', '')

            p4_ids_list = [
                x.strip()
                for x in p4_ids.split(',')
                if x.strip()
            ]

            # get P4 objects
            p4_objects = P4ID.objects.filter(
                p4_id__in=p4_ids_list
            )

            # save many-to-many
            p8.p4_ids.set(p4_objects)

            return redirect('p8_display_list')

    else:

        form = P8IDForm()

    return render(
        request,
        'installation/p8_entry.html',
        {
            'form': form
        }
    )

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
# ================= DISPLAY =================
def p8_list(request):

    data = P8ID.objects.prefetch_related(
        'p4_ids'
    ).order_by('-id')

    return render(
        request,
        'installation/p8_display_list.html',
        {
            'data': data
        }
    )

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
# ================= SEARCH P4 =================
def search_p4(request):

    q = request.GET.get('q', '').strip()

    results = P4ID.objects.filter(
        p4_id__icontains=q
    )[:10]

    data = [
        {
            "id": item.id,
            "p4_id": item.p4_id
        }
        for item in results
    ]

    return JsonResponse(data, safe=False)

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
# ================= EDIT =================
def p8_edit(request, id):

    p8 = get_object_or_404(P8ID, id=id)

    if request.method == 'POST':

        form = P8IDForm(
            request.POST,
            instance=p8
        )

        if form.is_valid():

            p8 = form.save()

            # update many-to-many
            p4_ids = request.POST.get('p4_ids', '')

            p4_ids_list = [
                x.strip()
                for x in p4_ids.split(',')
                if x.strip()
            ]

            p4_objects = P4ID.objects.filter(
                p4_id__in=p4_ids_list
            )

            p8.p4_ids.set(p4_objects)

            return redirect('p8_display_list')

    else:

        form = P8IDForm(instance=p8)

    return render(
        request,
        'installation/p8_entry.html',
        {
            'form': form,
            'p8': p8
        }
    )

@login_required
@role_required(['admin'])
# ================= DELETE =================
def p8_delete(request, id):

    p8 = get_object_or_404(P8ID, id=id)

    p8.delete()

    return redirect('p8_display_list')



from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .forms import P9IDForm
from .models import P9ID, P8ID

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
# ================= CREATE =================
def p9_create(request):

    if request.method == 'POST':

        form = P9IDForm(request.POST)

        if form.is_valid():

            p9 = form.save()

            # selected p8 ids
            p8_ids = request.POST.get('p8_ids', '')

            p8_ids_list = [
                x.strip()
                for x in p8_ids.split(',')
                if x.strip()
            ]

            # get P8 objects
            p8_objects = P8ID.objects.filter(
                p8_id__in=p8_ids_list
            )

            # save many-to-many
            p9.p8_ids.set(p8_objects)

            return redirect('p9_display_list')

    else:

        form = P9IDForm()

    return render(
        request,
        'installation/p9_entry.html',
        {
            'form': form
        }
    )

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
# ================= DISPLAY =================
def p9_list(request):

    data = P9ID.objects.prefetch_related(
        'p8_ids'
    ).order_by('-id')

    return render(
        request,
        'installation/p9_display_list.html',
        {
            'data': data
        }
    )

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
# ================= SEARCH P8 =================
def search_p8(request):

    q = request.GET.get('q', '').strip()

    results = P8ID.objects.filter(
        p8_id__icontains=q
    )[:10]

    data = [
        {
            "id": item.id,
            "p8_id": item.p8_id
        }
        for item in results
    ]

    return JsonResponse(data, safe=False)


# ================= EDIT =================
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p9_edit(request, id):

    p9 = get_object_or_404(P9ID, id=id)

    if request.method == 'POST':

        form = P9IDForm(
            request.POST,
            instance=p9
        )

        if form.is_valid():

            p9 = form.save()

            # update many-to-many
            p8_ids = request.POST.get('p8_ids', '')

            p8_ids_list = [
                x.strip()
                for x in p8_ids.split(',')
                if x.strip()
            ]

            p8_objects = P8ID.objects.filter(
                p8_id__in=p8_ids_list
            )

            p9.p8_ids.set(p8_objects)

            return redirect('p9_display_list')

    else:

        form = P9IDForm(instance=p9)

    return render(
        request,
        'installation/p9_entry.html',
        {
            'form': form,
            'p9': p9
        }
    )

@login_required
@role_required(['admin'])
# ================= DELETE =================
def p9_delete(request, id):

    p9 = get_object_or_404(P9ID, id=id)

    p9.delete()

    return redirect('p9_display_list')


from django.shortcuts import render

from .models import (
    Installation,
    P4ID,
    P8ID,
    P9ID
)

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def facility_dashboard_all(request):

    facility_data = {}

    # ================= INSTALLATIONS =================
    installations = Installation.objects.all().order_by(
        'facility',
        'system'
    )

    for ins in installations:

        facility = ins.facility
        system = ins.system

        # ================= DEFAULT STATUS =================
        f2_completed = False
        p4_completed = False
        p8_completed = False
        p9_completed = False

        # ================= F2 STATUS =================
        if ins.status:

            if ins.status.lower() in [
                'complete',
                'completed',
                'done'
            ]:

                f2_completed = True

        # ================= P4 =================
        p4_queryset = ins.p4_entries.all()

        if p4_queryset.filter(
            completed=True
        ).exists():

            p4_completed = True

        # ================= P8 =================
        p8_queryset = P8ID.objects.filter(
            p4_ids__in=p4_queryset,
            completed=True
        ).distinct()

        if p8_queryset.exists():

            p8_completed = True

        # ================= P9 =================
        p9_queryset = P9ID.objects.filter(
            p8_ids__in=p8_queryset,
            completed=True
        ).distinct()

        if p9_queryset.exists():

            p9_completed = True

        # ================= CREATE FACILITY =================
        if facility not in facility_data:

            facility_data[facility] = []

        # ================= APPEND SYSTEM =================
        facility_data[facility].append({

            "system": system,

            "completed": f2_completed,

            "p4_completed": p4_completed,

            "p8_completed": p8_completed,

            "p9_completed": p9_completed,

            "installation_id": ins.id,

            "ms_id": ins.ms_id,

            "ms_id_full": ins.ms_id_full,
        })

    # ================= RENDER =================
    return render(

        request,

        'installation/facility_dashboard_all.html',

        {
            'facility_data': facility_data
        }
    )


from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import ExtractYear

from .models import P4ID, P8ID, P9ID

import json
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import ExtractYear

from .models import P4ID

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p4_dashboard(request):
    total_p4 = P4ID.objects.count()
    completed_p4 = P4ID.objects.filter(completed=True).count()
    pending_p4 = P4ID.objects.filter(completed=False).count()

    total_ms = (
        P4ID.objects
        .values("ms_ids")
        .exclude(ms_ids=None)
        .distinct()
        .count()
    )

    yearly = (
        P4ID.objects
        .filter(completed=True, end_date__isnull=False)
        .annotate(year=ExtractYear("end_date"))
        .values("year")
        .annotate(total=Count("id"))
        .order_by("year")
    )

    status_labels = ["Completed", "Pending"]
    status_values = [completed_p4, pending_p4]

    year_labels = [item["year"] for item in yearly]
    year_values = [item["total"] for item in yearly]

    return render(request, "installation/p4_dashboard.html", {
        "total_p4": total_p4,
        "completed_p4": completed_p4,
        "pending_p4": pending_p4,
        "total_ms": total_ms,

        "status_labels": json.dumps(status_labels),
        "status_values": json.dumps(status_values),
        "year_labels": json.dumps(year_labels),
        "year_values": json.dumps(year_values),
    })
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p8_dashboard(request):
    total_p8 = P8ID.objects.count()
    completed_p8 = P8ID.objects.filter(completed=True).count()
    pending_p8 = P8ID.objects.filter(completed=False).count()
    total_p4 = P8ID.objects.values("p4_ids").distinct().count()

    yearly = (
        P8ID.objects
        .filter(completed=True, end_date__isnull=False)
        .annotate(year=ExtractYear("end_date"))
        .values("year")
        .annotate(total=Count("id"))
        .order_by("year")
    )

    return render(request, "installation/p8_dashboard.html", {
        "total_p8": total_p8,
        "completed_p8": completed_p8,
        "pending_p8": pending_p8,
        "total_p4": total_p4,
        "status_labels": ["Completed", "Pending"],
        "status_values": [completed_p8, pending_p8],
        "year_labels": [x["year"] for x in yearly],
        "year_values": [x["total"] for x in yearly],
    })

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p9_dashboard(request):
    total_p9 = P9ID.objects.count()
    completed_p9 = P9ID.objects.filter(completed=True).count()
    pending_p9 = P9ID.objects.filter(completed=False).count()
    total_p8 = P9ID.objects.values("p8_ids").distinct().count()

    yearly = (
        P9ID.objects
        .filter(completed=True, end_date__isnull=False)
        .annotate(year=ExtractYear("end_date"))
        .values("year")
        .annotate(total=Count("id"))
        .order_by("year")
    )

    return render(request, "installation/p9_dashboard.html", {
        "total_p9": total_p9,
        "completed_p9": completed_p9,
        "pending_p9": pending_p9,
        "total_p8": total_p8,
        "status_labels": ["Completed", "Pending"],
        "status_values": [completed_p9, pending_p9],
        "year_labels": [x["year"] for x in yearly],
        "year_values": [x["total"] for x in yearly],
    })

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p4_dashboard_filter(request):
    filter_type = request.GET.get("type")
    chart = request.GET.get("chart")
    value = request.GET.get("value")

    if chart == "status":
        if value == "Completed":
            records = P4ID.objects.filter(completed=True)
            title = "Completed P4"
        elif value == "Pending":
            records = P4ID.objects.filter(completed=False)
            title = "Pending P4"
        else:
            records = P4ID.objects.all()
            title = "All P4"

    elif chart == "year":
        records = P4ID.objects.filter(
            completed=True,
            end_date__year=value
        )
        title = f"Completed P4 in {value}"

    elif filter_type == "completed":
        records = P4ID.objects.filter(completed=True)
        title = "Completed P4"

    elif filter_type == "pending":
        records = P4ID.objects.filter(completed=False)
        title = "Pending P4"

    elif filter_type == "ms":
        records = P4ID.objects.prefetch_related("ms_ids").all()
        title = "MS Linked P4"

    else:
        records = P4ID.objects.all()
        title = "All P4"

    return render(request, "installation/filter_page.html", {
        "title": title,
        "records": records,
    })


@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p8_dashboard_filter(request):
    filter_type = request.GET.get("type")
    chart = request.GET.get("chart")
    value = request.GET.get("value")

    if chart == "status":
        if value == "Completed":
            records = P8ID.objects.filter(completed=True)
            title = "Completed P8"
        elif value == "Pending":
            records = P8ID.objects.filter(completed=False)
            title = "Pending P8"
        else:
            records = P8ID.objects.all()
            title = "All P8"

    elif chart == "year":
        records = P8ID.objects.filter(
            completed=True,
            end_date__year=value
        )
        title = f"Completed P8 in {value}"

    elif filter_type == "completed":
        records = P8ID.objects.filter(completed=True)
        title = "Completed P8"

    elif filter_type == "pending":
        records = P8ID.objects.filter(completed=False)
        title = "Pending P8"

    elif filter_type == "p4":
        records = P8ID.objects.prefetch_related("p4_ids").all()
        title = "P4 Linked P8"

    else:
        records = P8ID.objects.all()
        title = "All P8"

    return render(request, "installation/filter_page.html", {
        "title": title,
        "records": records,
    })

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def p9_dashboard_filter(request):
    filter_type = request.GET.get("type")
    chart = request.GET.get("chart")
    value = request.GET.get("value")

    if chart == "status":
        if value == "Completed":
            records = P9ID.objects.filter(completed=True)
            title = "Completed P9"
        elif value == "Pending":
            records = P9ID.objects.filter(completed=False)
            title = "Pending P9"
        else:
            records = P9ID.objects.all()
            title = "All P9"

    elif chart == "year":
        records = P9ID.objects.filter(
            completed=True,
            end_date__year=value
        )
        title = f"Completed P9 in {value}"

    elif filter_type == "completed":
        records = P9ID.objects.filter(completed=True)
        title = "Completed P9"

    elif filter_type == "pending":
        records = P9ID.objects.filter(completed=False)
        title = "Pending P9"

    elif filter_type == "p8":
        records = P9ID.objects.prefetch_related("p8_ids").all()
        title = "P8 Linked P9"

    else:
        records = P9ID.objects.all()
        title = "All P9"

    return render(request, "installation/filter_page.html", {
        "title": title,
        "records": records,
    })