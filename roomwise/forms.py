from django import forms
from .models import Facility, Room, System, RoomWiseDevice


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = [
            'facility',
            'facility_title',
        ]


class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = [
            'system_code',
            'system_title',
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'room_kks',
            'room_title',
        ]


class RoomWiseDeviceForm(forms.ModelForm):
    class Meta:
        model = RoomWiseDevice
        fields = [
            'system',
            'device_kks',
            'device_title',
            'telephone_number',
            'ms_id',
        ]


from django import forms
from .models import System


class BulkDeviceForm(forms.Form):

    system = forms.ModelChoiceField(
        queryset=System.objects.all()
    )

    ms_id = forms.CharField(
        max_length=100
    )


from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = '__all__'