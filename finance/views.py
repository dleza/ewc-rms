from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import BudgetPlan
from .reports import budget_vs_actual

def reports_home(request):
    return render(request, "finance/reports/home.html")

def budget_vs_actual_view(request, plan_id):
    plan = get_object_or_404(BudgetPlan, id=plan_id)
    ctx = budget_vs_actual(plan)
    ctx["plan"] = plan
    return render(request, "finance/reports/budget_vs_actual.html", ctx)
from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BudgetCategory, BudgetPlan, BudgetLine, Expense, MeetingCollection
from .forms import (
    BudgetCategoryForm, BudgetPlanForm, BudgetLineForm,
    ExpenseForm, MeetingCollectionForm
)


# -----------------------
# Budget Categories
# -----------------------
class CategoryListView(LoginRequiredMixin, ListView):
    model = BudgetCategory
    paginate_by = 20
    template_name = "finance/categories_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class CategoryCreateView(CreateView):
    model = BudgetCategory
    form_class = BudgetCategoryForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("finance:categories_list")

    def form_valid(self, form):
        messages.success(self.request, "Category saved.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "New Budget Category"
        ctx["cancel_url"] = reverse_lazy("finance:categories_list")
        return ctx


class CategoryUpdateView(UpdateView):
    model = BudgetCategory
    form_class = BudgetCategoryForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("finance:categories_list")

    def form_valid(self, form):
        messages.success(self.request, "Category updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Edit Budget Category"
        ctx["cancel_url"] = reverse_lazy("finance:categories_list")
        return ctx


# -----------------------
# Budget Plans
# -----------------------
class PlanListView(ListView):
    model = BudgetPlan
    paginate_by = 20
    template_name = "finance/plans_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        ptype = self.request.GET.get("period_type")
        if q:
            qs = qs.filter(Q(name__icontains=q))
        if ptype:
            qs = qs.filter(period_type=ptype)
        return qs


class PlanCreateView(CreateView):
    model = BudgetPlan
    form_class = BudgetPlanForm
    template_name = "generic/form.html"

    def get_success_url(self):
        return reverse("finance:plans_detail", args=[self.object.id])

    def form_valid(self, form):
        messages.success(self.request, "Budget plan created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "New Budget Plan"
        ctx["cancel_url"] = reverse_lazy("finance:plans_list")
        return ctx


class PlanUpdateView(UpdateView):
    model = BudgetPlan
    form_class = BudgetPlanForm
    template_name = "generic/form.html"

    def get_success_url(self):
        return reverse("finance:plans_detail", args=[self.object.id])

    def form_valid(self, form):
        messages.success(self.request, "Budget plan updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Edit Budget Plan"
        ctx["cancel_url"] = reverse("finance:plans_detail", args=[self.object.id])
        return ctx


class PlanDetailView(DetailView):
    model = BudgetPlan
    template_name = "finance/plans_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["line_form"] = BudgetLineForm()
        ctx["lines"] = self.object.lines.select_related("category").all()
        return ctx


def add_budget_line(request, plan_id):
    plan = get_object_or_404(BudgetPlan, id=plan_id)
    if request.method != "POST":
        return redirect("finance:plans_detail", pk=plan.id)

    form = BudgetLineForm(request.POST)
    if form.is_valid():
        line = form.save(commit=False)
        line.plan = plan
        try:
            line.save()
            messages.success(request, "Budget line added.")
        except Exception:
            messages.error(request, "This category already exists in the plan.")
    else:
        messages.error(request, "Please correct the errors and try again.")

    return redirect("finance:plans_detail", pk=plan.id)


def delete_budget_line(request, plan_id, line_id):
    plan = get_object_or_404(BudgetPlan, id=plan_id)
    line = get_object_or_404(BudgetLine, id=line_id, plan=plan)
    if request.method == "POST":
        line.delete()
        messages.success(request, "Budget line removed.")
    return redirect("finance:plans_detail", pk=plan.id)


# -----------------------
# Expenses
# -----------------------
class ExpenseListView(ListView):
    model = Expense
    paginate_by = 25
    template_name = "finance/expenses_list.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related("category")
        q = self.request.GET.get("q")
        category = self.request.GET.get("category")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        if q:
            qs = qs.filter(
                Q(description__icontains=q) |
                Q(paid_to__icontains=q) |
                Q(reference_no__icontains=q) |
                Q(recorded_by__icontains=q)
            )
        if category:
            qs = qs.filter(category_id=category)
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = BudgetCategory.objects.filter(is_active=True)
        ctx["total_amount"] = self.get_queryset().aggregate(total=Sum("amount"))["total"] or 0
        return ctx


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("finance:expenses_list")

    def form_valid(self, form):
        messages.success(self.request, "Expense saved.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "New Expense"
        ctx["cancel_url"] = reverse_lazy("finance:expenses_list")
        return ctx


class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("finance:expenses_list")

    def form_valid(self, form):
        messages.success(self.request, "Expense updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Edit Expense"
        ctx["cancel_url"] = reverse_lazy("finance:expenses_list")
        return ctx


# -----------------------
# Collections
# -----------------------
class CollectionListView(ListView):
    model = MeetingCollection
    paginate_by = 25
    template_name = "finance/collections_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        ctx["sum_offering"] = qs.aggregate(s=Sum("total_offering"))["s"] or 0
        ctx["sum_tithe"] = qs.aggregate(s=Sum("total_tithe"))["s"] or 0
        ctx["sum_first_fruits"] = qs.aggregate(s=Sum("total_first_fruits"))["s"] or 0
        ctx["sum_seed"] = qs.aggregate(s=Sum("total_seed_offering"))["s"] or 0
        return ctx


class CollectionCreateView(CreateView):
    model = MeetingCollection
    form_class = MeetingCollectionForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("finance:collections_list")

    def form_valid(self, form):
        messages.success(self.request, "Collection saved.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "New Meeting Collection"
        ctx["cancel_url"] = reverse_lazy("finance:collections_list")
        return ctx


class CollectionUpdateView(UpdateView):
    model = MeetingCollection
    form_class = MeetingCollectionForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("finance:collections_list")

    def form_valid(self, form):
        messages.success(self.request, "Collection updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Edit Meeting Collection"
        ctx["cancel_url"] = reverse_lazy("finance:collections_list")
        return ctx
