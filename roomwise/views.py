from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.deletion import ProtectedError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from common.decorators import role_required

from .models import Room, RoomWiseDevice, Equipment, Facility, System

from .forms import RoomForm, RoomWiseDeviceForm,FacilityForm, SystemForm

# ---------------- FACILITY ----------------

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def facility_add(request):
    form = FacilityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('facility_list')
    return render(request, 'roomwise/facility_form.html', {'form': form})

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def facility_list(request):
    data = Facility.objects.all()
    return render(request, 'roomwise/facility_list.html', {'data': data})


@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def facility_edit(request, pk):

    facility = get_object_or_404(
        Facility,
        pk=pk
    )

    form = FacilityForm(
        request.POST or None,
        instance=facility
    )

    if form.is_valid():
        form.save()
        return redirect('facility_list')

    return render(
        request,
        'roomwise/facility_form.html',
        {
            'form': form
        }
    )


@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def facility_delete(request, pk):

    facility = get_object_or_404(
        Facility,
        pk=pk
    )

    try:
        facility.delete()

        messages.success(
            request,
            f'Facility "{facility.facility}" deleted successfully.'
        )

    except ProtectedError:

        messages.error(
            request,
            f'Cannot delete Facility "{facility.facility}" because rooms are assigned to it. '
            f'Please delete or reassign the rooms first.'
        )

    return redirect('facility_list')


# ---------------- SYSTEM ----------------
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def system_add(request):
    form = SystemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('system_list')
    return render(request, 'roomwise/system_form.html', {'form': form})

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def system_list(request):
    data = System.objects.all()
    return render(request, 'roomwise/system_list.html', {'data': data})


# ---------------- ROOM ----------------
@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def room_add(request, facility_id):

    facility = get_object_or_404(
        Facility,
        pk=facility_id
    )

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)
            room.facility = facility
            room.save()

            return redirect(
                'facility_rooms',
                facility_id=facility.fid
            )
    else:
        form = RoomForm()

    return render(
        request,
        'roomwise/room_form.html',
        {
            'form': form,
            'facility': facility
        }
    )

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def room_list(request):
    facilities = Facility.objects.all()

    facility_id = request.GET.get('facility')

    rooms = None
    selected_facility = None

    if facility_id:
        selected_facility = get_object_or_404(
            Facility,
            pk=facility_id
        )

        rooms = Room.objects.filter(
            facility=selected_facility
        )

    return render(
        request,
        'roomwise/room_list.html',
        {
            'facilities': facilities,
            'rooms': rooms,
            'selected_facility': selected_facility,
        }
    )


@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def room_edit(request, pk):

    room = get_object_or_404(
        Room,
        pk=pk
    )

    facility_id = room.facility.fid

    form = RoomForm(
        request.POST or None,
        instance=room
    )

    if form.is_valid():

        updated_room = form.save(commit=False)

        # keep existing facility
        updated_room.facility = room.facility

        updated_room.save()

        return redirect(
            'facility_rooms',
            facility_id=facility_id
        )

    return render(
        request,
        'roomwise/room_form.html',
        {
            'form': form,
            'facility': room.facility
        }
    )

@login_required
@role_required(['admin'])
def room_delete(request, pk):

    room = get_object_or_404(
        Room,
        pk=pk
    )

    facility_id = room.facility.fid

    try:

        room.delete()

        messages.success(
            request,
            f'Room "{room.room_kks}" deleted successfully.'
        )

    except ProtectedError:

        messages.error(
            request,
            f'Cannot delete Room "{room.room_kks}" because device(s) are assigned to this room. '
            f'Please delete or move the devices first.'
        )

    return redirect(
        'facility_rooms',
        facility_id=facility_id
    )

# ---------------- DEVICE ----------------
from django.shortcuts import render, get_object_or_404
from .models import (
    Facility,
    Room,
    System,
    RoomWiseDevice,
    Equipment
)

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def device_add(request, facility_id):

    facility = get_object_or_404(Facility, pk=facility_id)

    rooms = Room.objects.filter(facility=facility)
    systems = System.objects.filter(facilitysystem__facility=facility).distinct()

    success = False

    # =========================
    # SAVE MULTIPLE DEVICES
    # =========================
    if request.method == "POST":

        system_id = request.POST.get("system")
        ms_id = request.POST.get("ms_id")

        system = get_object_or_404(System, pk=system_id)

        for room in rooms:

            kks_list = request.POST.getlist(
                f"device_kks_{room.rmid}[]"
            )

            title_list = request.POST.getlist(
                f"device_title_{room.rmid}[]"
            )

            telephone_list = request.POST.getlist(
                f"telephone_{room.rmid}[]"
            )

            # Remove old entries for this room/system
            RoomWiseDevice.objects.filter(
                system=system,
                room=room
            ).delete()

            total_rows = max(
                len(kks_list),
                len(title_list),
                len(telephone_list)
            )

            for i in range(total_rows):

                kks = (
                    kks_list[i].strip()
                    if i < len(kks_list)
                    else ""
                )

                title = (
                    title_list[i].strip()
                    if i < len(title_list)
                    else ""
                )

                telephone = (
                    telephone_list[i].strip()
                    if i < len(telephone_list)
                    else ""
                )

                if not (kks or title or telephone):
                    continue

                RoomWiseDevice.objects.create(
                    system=system,
                    room=room,
                    device_kks=kks,
                    device_title=title,
                    telephone_number=telephone,
                    ms_id=ms_id
                )

        success = True

    # =========================
    # LOAD EXISTING DATA
    # =========================
    system_data = []

    for system in systems:

        room_list = []
        equipments = Equipment.objects.filter(system=system)

        for room in rooms:

            devices = RoomWiseDevice.objects.filter(
                system=system,
                room=room
            )

            room_list.append({
                "room": room,
                "devices": devices,
            })

        system_data.append({
            "system": system,
            "rooms": room_list,
            "equipments": equipments,
        })

    return render(
        request,
        "roomwise/device_form.html",
        {
            "facility": facility,
            "system_data": system_data,
            "success": success,
        }
    )

@login_required
@role_required(['admin', 'manager', 'staff', 'viewer'])
def device_list(request):
    facilities = Facility.objects.all()
    search = request.GET.get('search', '')
    if search:
        facilities = facilities.filter(
            facility__icontains=search
        )

    facility_id = request.GET.get('facility')

    rooms = None
    selected_facility = None

    if facility_id:
        selected_facility = get_object_or_404(
            Facility,
            pk=facility_id
        )

        rooms = Room.objects.filter(
            facility=selected_facility
        )

    return render(
        request,
        'roomwise/device_list.html',
        {
            'facilities': facilities,
            'rooms': rooms,
            'selected_facility': selected_facility,
            'search': search,
        }
    )





def facility_rooms(request, facility_id):

    facility = get_object_or_404(
        Facility,
        pk=facility_id
    )

    rooms = Room.objects.filter(
        facility=facility
    )

    return render(
        request,
        'roomwise/facility_rooms.html',
        {
            'facility': facility,
            'rooms': rooms,
        }
    )




def bulk_device_add(request, facility_id):

    facility = get_object_or_404(
        Facility,
        pk=facility_id
    )

    rooms = Room.objects.filter(
        facility=facility
    )

    systems = System.objects.all()

    if request.method == "POST":

        block_count = int(
            request.POST.get("block_count", 1)
        )

        for block in range(block_count):

            system_id = request.POST.get(
                f"system_{block}"
            )

            ms_id = request.POST.get(
                f"ms_id_{block}"
            )

            if not system_id:
                continue

            system = System.objects.get(
                pk=system_id
            )

            for room in rooms:

                room_id = room.rmid

                device_kks_list = request.POST.getlist(
                    f"device_kks_{block}_{room_id}"
                )

                device_title_list = request.POST.getlist(
                    f"device_title_{block}_{room_id}"
                )

                for kks, title in zip(
                    device_kks_list,
                    device_title_list
                ):

                    if kks.strip():

                        RoomWiseDevice.objects.create(
                            room=room,
                            system=system,
                            ms_id=ms_id,
                            device_kks=kks,
                            device_title=title
                        )

        return redirect(
            'facility_rooms',
            facility_id=facility.fid
        )

    return render(
        request,
        'roomwise/bulk_device_form.html',
        {
            'facility': facility,
            'rooms': rooms,
            'systems': systems
        }
    )


def equipment_add(request, system_id):

    system = get_object_or_404(
        System,
        pk=system_id
    )

    if request.method == 'POST':

        equipment_name = request.POST.get(
            'equipment_name'
        )

        if equipment_name:
            Equipment.objects.create(
                system=system,
                equipment_name=equipment_name
            )

        return redirect(
            'equipment_add',
            system_id=system.sid
        )

    equipments = Equipment.objects.filter(
        system=system
    ).order_by('equipment_name')

    return render(
        request,
        'roomwise/equipment_add.html',
        {
            'system': system,
            'equipments': equipments,
        }
    )

def equipment_edit(request, pk):

    equipment = get_object_or_404(
        Equipment,
        pk=pk
    )

    if request.method == 'POST':

        equipment.equipment_name = request.POST.get(
            'equipment_name'
        )

        equipment.save()

        return redirect(
            'equipment_add',
            system_id=equipment.system.sid
        )

    return render(
        request,
        'roomwise/equipment_edit.html',
        {
            'equipment': equipment
        }
    )


def equipment_delete(request, pk):

    equipment = get_object_or_404(
        Equipment,
        pk=pk
    )

    system_id = equipment.system.sid

    equipment.delete()

    return redirect(
        'equipment_add',
        system_id=system_id
    )


from django.shortcuts import get_object_or_404, render
from .models import Facility, Room, System, RoomWiseDevice


def device_view(request, facility_id):

    facility = get_object_or_404(Facility, pk=facility_id)

    rooms = Room.objects.filter(facility=facility)
    systems = System.objects.all()

    system_data = []

    for system in systems:

        room_list = []

        for room in rooms:

            devices = RoomWiseDevice.objects.filter(
                system=system,
                room=room
            )

            if devices.exists():

                room_list.append({
                    "room": room,
                    "devices": devices,
                })

        if room_list:

            first_device = RoomWiseDevice.objects.filter(
                system=system,
                room__facility=facility
            ).first()

            system_data.append({
                "system": system,
                "rooms": room_list,
                "ms_id": first_device.ms_id if first_device else "",
            })

    return render(
        request,
        "roomwise/device_view.html",
        {
            "facility": facility,
            "system_data": system_data,
        }
    )




from .models import (
    Facility,
    System,
    FacilitySystem
)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
def facility_system_setup(request, fid):

    facility = get_object_or_404(Facility, pk=fid)
    systems = System.objects.all()

    if request.method == "POST":

        selected_ids = request.POST.getlist("systems")

        # prevent duplicate save
        FacilitySystem.objects.filter(facility=facility).delete()

        system_objects = System.objects.filter(sid__in=selected_ids)

        FacilitySystem.objects.bulk_create([
            FacilitySystem(facility=facility, system=s)
            for s in system_objects
        ])

        # build system names properly
        system_names = ", ".join(
            f"{s.system_code} - {s.system_title}"
            for s in system_objects
        )

        messages.success(
            request,
            f"Assigned to {facility.facility} ({facility.facility_title}): {system_names}"
        )

        return redirect("facility_system_setup", fid=facility.fid)

    selected_ids = FacilitySystem.objects.filter(
        facility=facility
    ).values_list("system_id", flat=True)

    return render(request, "roomwise/facility_system_setup.html", {
        "facility": facility,
        "systems": systems,
        "selected_ids": list(selected_ids),
    })