from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import BudgetPlan
from .reports import budget_vs_actual, collections_vs_expenses, monthly_expenditure
from .forms_reports import DateRangeReportForm, YearReportForm


def reports_home(request):
    plans = BudgetPlan.objects.all()[:10]
    return render(request, "finance/reports/home.html", {"plans": plans})


def budget_vs_actual_view(request, plan_id):
    plan = get_object_or_404(BudgetPlan, id=plan_id)
    ctx = budget_vs_actual(plan)
    ctx["plan"] = plan
    return render(request, "finance/reports/budget_vs_actual.html", ctx)


def collections_vs_expenses_view(request):
    form = DateRangeReportForm(request.GET or None)
    report = None

    if form.is_valid():
        date_from = form.cleaned_data["date_from"]
        date_to = form.cleaned_data["date_to"]
        report = collections_vs_expenses(date_from, date_to)
        report["date_from"] = date_from
        report["date_to"] = date_to
    elif request.GET:
        messages.error(request, "Please correct the date range.")

    return render(request, "finance/reports/collections_vs_expenses.html", {"form": form, "report": report})


def monthly_expenditure_view(request):
    form = YearReportForm(request.GET or None, initial={"year": timezone.now().year})
    report = None

    if form.is_valid():
        year = form.cleaned_data["year"]
        report = monthly_expenditure(year)
        report["year"] = year
    elif request.GET:
        messages.error(request, "Please enter a valid year.")

    return render(request, "finance/reports/monthly_expenditure.html", {"form": form, "report": report})
