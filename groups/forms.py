from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["group_type", "name", "leader"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class GroupMembersForm(forms.Form):
    """
    Checkbox list of all members for assignment.
    """
    members = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        member_qs = kwargs.pop("member_qs")
        super().__init__(*args, **kwargs)
        self.fields["members"].queryset = member_qs
