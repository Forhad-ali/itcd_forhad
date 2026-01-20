from django.db import models
from django import forms
from .models import EquipmentEntry
from .models import System
from .models import Learning_Category 
from .models import TopicsEntry
class EquipmentEntryForm(forms.ModelForm):
    class Meta:
        model = EquipmentEntry
        fields = ['equipment_name', 'equipment_brand', 'type']
        widgets = {
            'equipment_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipment Name'}),
            'equipment_brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand Name'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }


class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = ['code', 'title']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'text-transform: uppercase;',
                'placeholder': 'Enter Code'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'text-transform: uppercase;',
                'placeholder': 'Enter Title'
            }),
        }

    def clean_code(self):
        return self.cleaned_data['code'].upper()

    def clean_title(self):
        return self.cleaned_data['title'].upper()



# entry/forms.py

from django import forms
from .models import EquipmentDocument

class EquipmentDocumentForm(forms.ModelForm):
    class Meta:
        model = EquipmentDocument
        fields = ['code', 'title', 'description', 'image']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

from .models import Facility

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['code', 'title', 'type']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control text-uppercase'}),
            'title': forms.TextInput(attrs={'class': 'form-control text-uppercase'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }



# forms.py
# forms.py
from django import forms
from .models import System

class AssignSystemForm(forms.Form):
    systems = forms.ModelMultipleChoiceField(
        queryset=System.objects.all(),  # ✅ Show all systems
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select systems to assign to this facility"
    )

    def __init__(self, *args, **kwargs):
        facility = kwargs.pop('facility', None)
        super().__init__(*args, **kwargs)

        if facility:
            # Optional: Pre-select already assigned systems for this facility
            self.fields['systems'].initial = System.objects.filter(facility=facility)


#MS Incoming Act
from .models import MSIncoActEntry
class MSIncoActEntryForm(forms.ModelForm):
    class Meta:
        model = MSIncoActEntry
        fields = ['ms_id', 'incoming_act']

#Learning Category
class LearningCategoryForm(forms.ModelForm):
    class Meta:
        model = Learning_Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Learning Category'
            }),
        }

class TopicsEntryForm(forms.ModelForm):
    class Meta:
        model = TopicsEntry
        fields = ['topics']
        widgets = {
            'topics': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topics'}),

        }


