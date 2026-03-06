from django import forms
from django.utils import timezone


class DateRangeReportForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))


class YearReportForm(forms.Form):
    year = forms.IntegerField(
        initial=timezone.now().year,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "2000", "max": "2100"})
    )
