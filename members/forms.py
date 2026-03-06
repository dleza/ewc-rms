from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = "__all__"
        widgets = {
            "date_of_join": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_of_renewal": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ("date_of_join", "date_of_renewal"):
                css = "form-select" if field.widget.__class__.__name__ == "Select" else "form-control"
                field.widget.attrs["class"] = css
