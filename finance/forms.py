from django import forms
from django.forms import inlineformset_factory
from .models import (
    BudgetCategory, BudgetPlan, BudgetLine, Expense,
    MeetingCollection, CollectionEntry
)


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class BudgetCategoryForm(BootstrapModelForm):
    class Meta:
        model = BudgetCategory
        fields = ["name", "is_active"]


class BudgetPlanForm(BootstrapModelForm):
    class Meta:
        model = BudgetPlan
        fields = ["period_type", "name", "start_date", "end_date", "approved_by", "approved_on"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "approved_on": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class BudgetLineForm(BootstrapModelForm):
    class Meta:
        model = BudgetLine
        fields = ["category", "amount_allocated"]


class ExpenseForm(BootstrapModelForm):
    class Meta:
        model = Expense
        fields = ["date", "category", "description", "amount", "paid_to", "reference_no", "recorded_by"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class MeetingCollectionForm(BootstrapModelForm):
    class Meta:
        model = MeetingCollection
        fields = ["date", "name_of_counter", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


class CollectionEntryForm(BootstrapModelForm):
    class Meta:
        model = CollectionEntry
        fields = ["category", "amount"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].widget.attrs.update({"min": 0, "step": "0.01"})


CollectionEntryFormSet = inlineformset_factory(
    MeetingCollection,
    CollectionEntry,
    form=CollectionEntryForm,
    extra=0,
    can_delete=True
)