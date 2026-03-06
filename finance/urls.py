from django.urls import path
from . import views
from .views_collections import CollectionListView, collection_create, collection_update
from . import views_reports

app_name = "finance"

urlpatterns = [
    # Categories
    path("categories/", views.CategoryListView.as_view(), name="categories_list"),
    path("categories/new/", views.CategoryCreateView.as_view(), name="categories_create"),
    path("categories/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="categories_update"),

    # Budget Plans
    path("budgets/", views.PlanListView.as_view(), name="plans_list"),
    path("budgets/new/", views.PlanCreateView.as_view(), name="plans_create"),
    path("budgets/<int:pk>/", views.PlanDetailView.as_view(), name="plans_detail"),
    path("budgets/<int:pk>/edit/", views.PlanUpdateView.as_view(), name="plans_update"),

    # Budget Lines
    path("budgets/<int:plan_id>/lines/add/", views.add_budget_line, name="plan_line_add"),
    path("budgets/<int:plan_id>/lines/<int:line_id>/delete/", views.delete_budget_line, name="plan_line_delete"),

    # Expenses
    path("expenses/", views.ExpenseListView.as_view(), name="expenses_list"),
    path("expenses/new/", views.ExpenseCreateView.as_view(), name="expenses_create"),
    path("expenses/<int:pk>/edit/", views.ExpenseUpdateView.as_view(), name="expenses_update"),

    # Dynamic Collections
    path("collections/", CollectionListView.as_view(), name="collections_list"),
    path("collections/new/", collection_create, name="collections_create"),
    path("collections/<int:pk>/edit/", collection_update, name="collections_update"),

    # Reports
    path("reports/", views_reports.reports_home, name="reports_home"),
    path("reports/budget/<int:plan_id>/", views_reports.budget_vs_actual_view, name="budget_vs_actual"),
    path("reports/collections-vs-expenses/", views_reports.collections_vs_expenses_view, name="collections_vs_expenses"),
    path("reports/monthly-expenditure/", views_reports.monthly_expenditure_view, name="monthly_expenditure"),
]