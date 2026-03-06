from django import forms
from .models import AttendanceRecord


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = [
            "activity_type", "group", "date",
            "adult_female", "adult_male",
            "teen_female", "teen_male",
            "children_female", "children_male",
            "preacher", "title_of_msg",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                # number inputs a bit nicer
                if name in (
                    "adult_female","adult_male","teen_female","teen_male","children_female","children_male"
                ):
                    field.widget.attrs["class"] = "form-control"
                    field.widget.attrs["min"] = 0
                else:
                    field.widget.attrs["class"] = "form-control"

