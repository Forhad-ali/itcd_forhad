from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils.text import slugify
from django import forms
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from django.db.models import Q

import csv

from .forms import (
    EquipmentEntryForm, SystemForm, EquipmentDocumentForm, FacilityForm,
    LearningCategoryForm, TopicsEntryForm
)
from .models import (
    Facility, System, EquipmentEntry, EquipmentDocument,
    SystemEquipmentQuantity, SystemFacilityAssignment,
    Learning_Category, TopicsEntry, LearningStep, MSIncoActEntry
)

# ------------------------ System Views ------------------------

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def system_grid(request):
    systems = System.objects.all()
    return render(request, 'entry/system_display.html', {'systems': systems})

@login_required
@role_required(['admin', 'manager'])
def add_system(request):
    if request.method == 'POST':
        form = SystemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('system_grid')
    else:
        form = SystemForm()
    return render(request, 'entry/add_system.html', {'form': form})

# ------------------------ Equipment Views ------------------------

@login_required
@role_required(['admin', 'manager', 'staff'])
def equipment_entry(request, system_id):
    system = get_object_or_404(System, id=system_id)
    if request.method == 'POST':
        form = EquipmentEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.system = system
            entry.save()
            return redirect('equipment_entry', system_id=system.id)
    else:
        form = EquipmentEntryForm()

    entries = EquipmentEntry.objects.filter(system=system)

    return render(request, 'entry/equipment_entry.html', {
        'form': form,
        'system': system,
        'entries': entries,
    })

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def equipment_detail_view(request, equipment_id):
    equipment = get_object_or_404(EquipmentEntry, id=equipment_id)
    documents = EquipmentDocument.objects.filter(equipment=equipment)

    if documents.exists():
        return render(request, 'entry/equipment_detail_view.html', {
            'equipment': equipment,
            'documents': documents,
        })
    else:
        if request.method == 'POST':
            form = EquipmentDocumentForm(request.POST, request.FILES)
            if form.is_valid():
                doc = form.save(commit=False)
                doc.equipment = equipment
                doc.save()
                return redirect('equipment_detail_view', equipment_id=equipment.id)
        else:
            form = EquipmentDocumentForm()
        return render(request, 'entry/equipment_detail_entry.html', {
            'equipment': equipment,
            'form': form
        })

@login_required
@role_required(['admin', 'manager', 'staff'])
def edit_equipment(request, pk):
    entry = get_object_or_404(EquipmentEntry, pk=pk)
    if request.method == 'POST':
        form = EquipmentEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('equipment_entry', system_id=entry.system.id)
    else:
        form = EquipmentEntryForm(instance=entry)
    return render(request, 'entry/edit_equipment.html', {'form': form, 'entry': entry})

@login_required
@role_required(['admin', 'manager'])
def delete_equipment(request, pk):
    entry = get_object_or_404(EquipmentEntry, pk=pk)
    system_id = entry.system.id
    entry.delete()
    return redirect('equipment_entry', system_id=system_id)

@login_required
@role_required(['admin', 'manager', 'staff'])
def edit_equipment_detail(request, pk):
    equipment = get_object_or_404(EquipmentEntry, pk=pk)
    document = EquipmentDocument.objects.filter(equipment=equipment).first()

    if request.method == 'POST':
        form = EquipmentDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.equipment = equipment
            doc.save()
            return redirect('equipment_detail_view', equipment.id)
    else:
        form = EquipmentDocumentForm(instance=document)

    return render(request, 'entry/edit_equipment_detail.html', {
        'form': form,
        'equipment': equipment,
    })

# ------------------------ Facility Views ------------------------

@login_required
@role_required(['admin', 'manager'])
def add_facility(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facility_grid')
    else:
        form = FacilityForm()
    return render(request, 'entry/add_facility.html', {'form': form})

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def facility_grid(request):
    query = request.GET.get('q')
    if query:
        core_facilities = Facility.objects.filter(code__icontains=query, type='Core')
        terminal_facilities = Facility.objects.filter(code__icontains=query, type='Terminal')
    else:
        core_facilities = Facility.objects.filter(type='Core')
        terminal_facilities = Facility.objects.filter(type='Terminal')

    return render(request, 'entry/facility_grid.html', {
        'core_facilities': core_facilities,
        'terminal_facilities': terminal_facilities,
    })

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def facility_list(request):
    facilities = Facility.objects.all()
    return render(request, 'entry/facility_list.html', {'facilities': facilities})

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def systems_by_facility(request, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)
    assigned_system_ids = SystemFacilityAssignment.objects.filter(facility=facility).values_list('system_id', flat=True)
    systems = System.objects.filter(id__in=assigned_system_ids)
    return render(request, 'entry/systems_by_facility.html', {
        'facility': facility,
        'systems': systems
    })

# ------------------------ System-Facility Assignment ------------------------

class AssignSystemForm(forms.Form):
    systems = forms.ModelMultipleChoiceField(
        queryset=System.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select systems to assign"
    )

@login_required
@role_required(['admin', 'manager'])
def add_system_to_facility(request, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)
    if request.method == 'POST':
        form = SystemForm(request.POST)
        if form.is_valid():
            system = form.save()
            SystemFacilityAssignment.objects.create(system=system, facility=facility)
            return redirect('systems_by_facility', facility_id=facility.id)
    else:
        form = SystemForm()
    return render(request, 'entry/add_system_to_facility.html', {
        'form': form,
        'facility': facility
    })

@login_required
@role_required(['admin', 'manager'])
def assign_systems_to_facility(request, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)
    if request.method == 'POST':
        form = AssignSystemForm(request.POST)
        if form.is_valid():
            selected_systems = form.cleaned_data['systems']
            for system in selected_systems:
                SystemFacilityAssignment.objects.get_or_create(system=system, facility=facility)
            return redirect('systems_by_facility', facility_id=facility.id)
    else:
        form = AssignSystemForm()
    return render(request, 'entry/assign_systems_to_facility.html', {
        'facility': facility,
        'form': form,
    })

# ------------------------ System Equipment Quantity ------------------------

@login_required
@role_required(['admin', 'manager', 'staff'])
def system_equipment_quantity_view(request, system_id, facility_id):
    system = get_object_or_404(System, id=system_id)
    facility = get_object_or_404(Facility, id=facility_id)

    old_equipments = EquipmentEntry.objects.filter(system=system).values_list('equipment_name', flat=True).distinct()
    existing_entries = SystemEquipmentQuantity.objects.filter(system=system, facility=facility)
    entry_map = {entry.equipment_name: entry for entry in existing_entries}

    first_entry = existing_entries.first()
    doc_ref_value = first_entry.doc_reference_code if first_entry else ''
    doc_ver_value = first_entry.doc_version if first_entry else ''

    if request.method == 'POST':
        doc_ref = request.POST.get('doc_reference_code')
        doc_ver = request.POST.get('doc_version')
        for equipment_name in old_equipments:
            slug = slugify(equipment_name)
            qty_input = request.POST.get(f'quantity_{slug}')
            try:
                quantity = int(qty_input) if qty_input else None
            except ValueError:
                quantity = None

            if quantity is None or quantity == 0:
                SystemEquipmentQuantity.objects.filter(
                    system=system,
                    facility=facility,
                    equipment_name=equipment_name
                ).delete()
                continue

            try:
                equipment_entry_obj = EquipmentEntry.objects.get(system=system, equipment_name=equipment_name)
            except EquipmentEntry.DoesNotExist:
                equipment_entry_obj = None
            except EquipmentEntry.MultipleObjectsReturned:
                equipment_entry_obj = EquipmentEntry.objects.filter(system=system, equipment_name=equipment_name).first()

            SystemEquipmentQuantity.objects.update_or_create(
                system=system,
                facility=facility,
                equipment_name=equipment_name,
                defaults={
                    'quantity': quantity,
                    'doc_reference_code': doc_ref,
                    'doc_version': doc_ver,
                    'equipment_entry': equipment_entry_obj
                }
            )

        messages.success(request, "Quantities and document information saved successfully.")
        return redirect('system_equipment_quantity', system_id=system.id, facility_id=facility.id)

    equipment_list = []
    for name in old_equipments:
        entry = entry_map.get(name)
        equipment_list.append({
            'name': name,
            'quantity': entry.quantity if entry else None,
        })

    return render(request, 'entry/system_equipment_quantity.html', {
        'system': system,
        'facility': facility,
        'equipment_list': equipment_list,
        'doc_ref_value': doc_ref_value,
        'doc_ver_value': doc_ver_value,
    })

# ------------------------ Reports ------------------------

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def export_facility_equipment_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="facility_equipment_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Facility Code', 'Facility Title', 'System Code', 'System Title', 'Equipment Name', 'Quantity', 'Doc Ref', 'Doc Version'])
    assignments = SystemFacilityAssignment.objects.select_related('facility', 'system')
    for assignment in assignments:
        facility = assignment.facility
        system = assignment.system
        equipment_quantities = SystemEquipmentQuantity.objects.filter(system=system, facility=facility)
        for eq in equipment_quantities:
            writer.writerow([
                facility.code,
                facility.title,
                system.code,
                system.title,
                eq.equipment_name,
                eq.quantity if eq.quantity is not None else '',
                eq.doc_reference_code or '',
                eq.doc_version or ''
            ])
    return response

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])

def facility_equipment_report_view(request):
    selected_facility = request.GET.get('facility')
    selected_system = request.GET.get('system')
    selected_equipment = request.GET.get('equipment')
    selected_equipment_types = request.GET.getlist('equipment_type')

    # Base data for filters
    facilities = Facility.objects.all()
    systems = System.objects.all()
    equipment_names = SystemEquipmentQuantity.objects.values_list('equipment_name', flat=True).distinct()
    equipment_types = EquipmentEntry.objects.values_list('type', flat=True).distinct()

    report_data = []
    print("Selected types:", selected_equipment_types)

    # Filter facilities if selected
    facility_qs = facilities
    if selected_facility:
        facility_qs = facility_qs.filter(id=selected_facility)

    for fac in facility_qs:
        # Systems assigned to this facility
        system_qs = System.objects.filter(systemfacilityassignment__facility=fac).distinct()

        # Filter by selected system
        if selected_system:
            system_qs = system_qs.filter(id=selected_system)

        system_list = []

        for sys in system_qs:
            entries = SystemEquipmentQuantity.objects.filter(system=sys, facility=fac)
              # Debug counts - Add here
            total = entries.count()
            linked = entries.filter(equipment_entry__isnull=False).count()
            print(f"Facility: {fac.code}, System: {sys.code} => Total entries: {total}, linked to equipment_entry: {linked}")

            # Filter by selected equipment name
            if selected_equipment:
                entries = entries.filter(equipment_name=selected_equipment)

            # Exclude equipment entries whose equipment_entry.type is in selected_equipment_types
            if selected_equipment_types:
                entries = entries.filter(
                    Q(equipment_entry__isnull=True) |  # keep those with no equipment_entry
                    Q(equipment_entry__type__in=selected_equipment_types)  # exclude selected types
                )

            if entries.exists():
                system_list.append({
                    'system': sys,
                    'doc_ref': entries.first().doc_reference_code,
                    'doc_ver': entries.first().doc_version,
                    'equipments': [
                        {
                            'name': entry.equipment_name,
                            'quantity': entry.quantity,
                        } for entry in entries
                    ]
                })

        if system_list:
            report_data.append({
                'facility': fac,
                'systems': system_list
            })

    context = {
        'facilities': facilities,
        'systems': systems,
        'equipment_names': equipment_names,
        'equipment_types': equipment_types,
        'selected_facility': selected_facility,
        'selected_system': selected_system,
        'selected_equipment': selected_equipment,
        'selected_equipment_types': selected_equipment_types,
        'report_data': report_data,
    }

    return render(request, 'entry/facility_equipment_report.html', context)


@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def export_equipment_pdf(request):
    return HttpResponse("PDF export not implemented yet.", content_type="text/plain")

# ------------------------ MS Incoming ACT ------------------------

@login_required
@role_required(['admin', 'manager', 'staff'])
def ms_inco_act_entry_view(request):
    ms_id_filter = request.GET.get("ms_id_filter", "").strip()
    incoming_act_filter = request.GET.get("incoming_act_filter", "").strip()
    qs = MSIncoActEntry.objects.all()
    if ms_id_filter:
        qs = qs.filter(ms_id__icontains=ms_id_filter)
    if incoming_act_filter:
        qs = qs.filter(incoming_act__icontains=incoming_act_filter)
    grouped = {}
    for item in qs.order_by('ms_id', 'created_at'):
        grouped.setdefault(item.ms_id, []).append(item.incoming_act)
    grouped_entries = [{"ms_id": ms_id, "incoming_acts": acts} for ms_id, acts in grouped.items()]
    return render(request, "entry/ms_inco_act_entry.html", {"grouped_entries": grouped_entries})

@login_required
@role_required(['admin', 'manager', 'staff'])
def add_incoming_act_view(request):
    ms_id = request.POST.get("ms_id", "").strip()
    incoming_act = request.POST.get("incoming_act", "").strip()
    if ms_id and incoming_act:
        MSIncoActEntry.objects.create(ms_id=ms_id, incoming_act=incoming_act)
    return redirect("ms_inco_act_entry")

# ------------------------ Learning Category & Topics ------------------------

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def learning_category_display(request):
    learning_category = Learning_Category.objects.all()
    return render(request, 'entry/learning_category_display.html', {'learning_category': learning_category})

@login_required
@role_required(['admin', 'manager'])
def learning_category_add(request):
    if request.method == 'POST':
        form = LearningCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_category_display')
    else:
        form = LearningCategoryForm()
    return render(request, 'entry/learning_category_add.html', {'form': form})

@login_required
@role_required(['admin', 'manager', 'staff'])
def topics_entry(request, learning_category_id):
    learning_category = get_object_or_404(Learning_Category, id=learning_category_id)
    if request.method == 'POST':
        form = TopicsEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.learning_category = learning_category
            entry.save()
            return redirect('topics_entry', learning_category_id=learning_category.id)
    else:
        form = TopicsEntryForm()
    entries = TopicsEntry.objects.filter(learning_category=learning_category)
    return render(request, 'entry/learning_topics_entry.html', {
        'form': form,
        'learning_category': learning_category,
        'entries': entries,
    })

@login_required
@role_required(['admin', 'manager'])
def edit_topics(request, pk):
    entry = get_object_or_404(TopicsEntry, pk=pk)
    if request.method == 'POST':
        form = TopicsEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('topics_entry', learning_category_id=entry.learning_category_id)
    else:
        form = TopicsEntryForm(instance=entry)
    return render(request, 'entry/learning_topics_edit.html', {'form': form, 'entry': entry})

@login_required
@role_required(['admin', 'manager'])
def delete_topics(request, pk):
    entry = get_object_or_404(TopicsEntry, pk=pk)
    learning_category_id = entry.learning_category_id
    entry.delete()
    return redirect('topics_entry', learning_category_id=learning_category_id)

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def learning_steps_view(request, topic_id):
    topic = get_object_or_404(TopicsEntry, id=topic_id)
    if request.method == 'POST':
        step_count = int(request.POST.get('step_count', 0))
        for i in range(step_count):
            step_number = request.POST.get(f'step_number_{i}')
            title = request.POST.get(f'title_{i}')
            text = request.POST.get(f'text_{i}')
            if step_number and title and text:
                LearningStep.objects.create(
                    topics_entry=topic,
                    step_number=step_number,
                    title=title,
                    text=text
                )
        return redirect('learning_steps_view', topic_id=topic_id)
    steps = LearningStep.objects.filter(topics_entry=topic).order_by('step_number')
    return render(request, 'entry/learning_step_entry.html', {
        'steps': steps,
        'topic': topic,
    })

@login_required
@role_required(['admin', 'manager'])
def edit_step(request, step_id):
    step = get_object_or_404(LearningStep, id=step_id)
    if request.method == 'POST':
        step.step_number = request.POST.get('step_number')
        step.title = request.POST.get('title')
        step.text = request.POST.get('text')
        step.save()
        return redirect('learning_steps_view', topic_id=step.topics_entry.id)

@login_required
@role_required(['admin', 'manager'])
def delete_step(request, step_id):
    step = get_object_or_404(LearningStep, id=step_id)
    topic_id = step.topics_entry.id
    step.delete()
    return redirect('learning_steps_view', topic_id=topic_id)
