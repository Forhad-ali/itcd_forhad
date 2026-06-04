from django import forms
from .models import Installation


class InstallationForm(forms.ModelForm):

    # ================= STATUS =================
    STATUS_CHOICES = [
        ("Completed", "Completed"),
        ("Ongoing", "Ongoing"),
        ("Not Started Yet", "Not Started Yet"),
    ]


    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    TYPE_CHOICES = [
        ("TB", "TB"),
        ("MB", "MB"),
    ]

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    # ================= SYSTEM =================
    SYSTEM_CHOICES = [
        ("0", "0"),
        ("ACY", "ACY"),
        ("AYC", "AYC"),
        ("CYA", "CYA"),
        ("CYB", "CYB"),
        ("CYC", "CYC"),
        ("CYE", "CYE"),
        ("CYF", "CYF"),
        ("CYH", "CYH"),
        ("CYK", "CYK"),
        ("CYN", "CYN"),
        ("CYP", "CYP"),
        ("CYQ", "CYQ"),
        ("CYS", "CYS"),
        ("CYU", "CYU"),
        ("CYV", "CYV"),
        ("CYX", "CYX"),
        ("CYY", "CYY"),
        ("CYZ", "CYZ"),
    ]

    system = forms.ChoiceField(
        choices=SYSTEM_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # ================= UNIT =================
    UNIT_CHOICES = [
        ("U0", "U0"),
        ("U1", "U1"),
        ("U2", "U2"),
    ]

    unit = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # ================= STAGE =================
    STAGE_CHOICES = [
        ("ST00", "ST00"),
        ("ST01", "ST01"),
        ("ST02", "ST02"),
        ("ST03", "ST03"),
        ("ST04", "ST04"),
        ("ST05", "ST05"),
        ("ST06", "ST06"),
        ("ST07", "ST07"),
        ("ST08", "ST08"),
        ("ST09", "ST09"),
        ("ST10", "ST10"),
        ("ST11", "ST11"),
        ("ST12", "ST12"),
        ("ST13", "ST13"),
        ("ST14", "ST14"),
        ("ST15", "ST15"),
        ("ST16", "ST16"),
        ("ST17", "ST17"),
        ("ST18", "ST18"),

    ]

    stage = forms.ChoiceField(
        choices=STAGE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Installation
        fields = "__all__"

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


from django import forms
from .models import P4ID


class P4IDForm(forms.ModelForm):

    class Meta:

        model = P4ID

        fields = [
            'p4_id',
            'saw_programs',
            'associate_ms',
            'completed',
            'start_date',
            'end_date'
        ]

        widgets = {

            'p4_id': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'saw_programs': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'associate_ms': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }


from django import forms
from .models import P8ID


class P8IDForm(forms.ModelForm):

    class Meta:

        model = P8ID

        fields = [
            'p8_id',
            'p2_id',
            'completed',
            'start_date',
            'end_date'
        ]

        widgets = {

            'p8_id': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'p2_id': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
    


from django import forms
from .models import P9ID


class P9IDForm(forms.ModelForm):

    class Meta:

        model = P9ID

        fields = [
            'p9_id',
            'completed',
            'start_date',
            'end_date'
        ]

        widgets = {

            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'end_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }