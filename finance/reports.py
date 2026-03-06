from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import BudgetLine, Expense, MeetingCollection


def budget_vs_actual(plan):
    """
    For a given BudgetPlan:
    - allocated per category comes from BudgetLine
    - spent per category comes from Expense within plan date range
    """
    lines = (
        BudgetLine.objects
        .filter(plan=plan)
        .select_related("category")
        .order_by("category__name")
    )

    spent_map = dict(
        Expense.objects
        .filter(date__range=(plan.start_date, plan.end_date))
        .values("category")
        .annotate(spent=Sum("amount"))
        .values_list("category", "spent")
    )

    rows = []
    total_alloc = Decimal("0.00")
    total_spent = Decimal("0.00")

    for line in lines:
        spent = spent_map.get(line.category_id) or Decimal("0.00")
        allocated = line.amount_allocated
        variance = allocated - spent

        rows.append({
            "category": line.category.name,
            "allocated": allocated,
            "spent": spent,
            "variance": variance,
            "is_over": spent > allocated,
        })

        total_alloc += allocated
        total_spent += spent

    return {
        "rows": rows,
        "total_allocated": total_alloc,
        "total_spent": total_spent,
        "total_variance": total_alloc - total_spent,
    }


def collections_vs_expenses(date_from, date_to):
    """
    Date range report:
    - total collections (offering+tithe+first_fruits+seed)
    - total expenses
    - net difference
    """
    collections_qs = MeetingCollection.objects.filter(date__range=(date_from, date_to))
    expenses_qs = Expense.objects.filter(date__range=(date_from, date_to))

    sums = collections_qs.aggregate(
        offering=Sum("total_offering"),
        tithe=Sum("total_tithe"),
        first_fruits=Sum("total_first_fruits"),
        seed=Sum("total_seed_offering"),
    )

    offering = sums["offering"] or Decimal("0.00")
    tithe = sums["tithe"] or Decimal("0.00")
    first_fruits = sums["first_fruits"] or Decimal("0.00")
    seed = sums["seed"] or Decimal("0.00")

    total_collections = offering + tithe + first_fruits + seed
    total_expenses = expenses_qs.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    return {
        "offering": offering,
        "tithe": tithe,
        "first_fruits": first_fruits,
        "seed": seed,
        "total_collections": total_collections,
        "total_expenses": total_expenses,
        "net": total_collections - total_expenses,
        "collections_count": collections_qs.count(),
        "expenses_count": expenses_qs.count(),
    }


def monthly_expenditure(year: int):
    """
    Return total expenses per month in a given year.
    """
    qs = (
        Expense.objects
        .filter(date__year=year)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    rows = []
    grand_total = Decimal("0.00")
    for r in qs:
        rows.append({
            "month": r["month"],
            "total": r["total"] or Decimal("0.00"),
        })
        grand_total += r["total"] or Decimal("0.00")

    return {"rows": rows, "grand_total": grand_total}
