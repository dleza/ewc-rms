""" from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

from members.models import Member
from groups.models import Group
from visitors.models import Visitor
from services.models import AttendanceRecord
from finance.models import Expense, MeetingCollection


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        today = timezone.localdate()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        total_members = Member.objects.count()
        total_groups = Group.objects.count()

        visitors_this_week = Visitor.objects.filter(date__gte=start_of_week, date__lte=today).count()

        attendance_qs = AttendanceRecord.objects.filter(date__gte=start_of_week, date__lte=today)
        attendance_total = 0
        for a in attendance_qs:
            attendance_total += a.total_attendance

        collections_this_week = Decimal("0.00")
        collections_qs = MeetingCollection.objects.filter(date__gte=start_of_week, date__lte=today)
        for c in collections_qs:
            collections_this_week += c.total

        expenses_this_month = (
            Expense.objects
            .filter(date__gte=start_of_month, date__lte=today)
            .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        )

        expenses_this_week = (
            Expense.objects
            .filter(date__gte=start_of_week, date__lte=today)
            .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        )

        net_this_week = collections_this_week - expenses_this_week

        ctx.update({
            "today": today,
            "total_members": total_members,
            "total_groups": total_groups,
            "visitors_this_week": visitors_this_week,
            "attendance_this_week": attendance_total,
            "collections_this_week": collections_this_week,
            "expenses_this_month": expenses_this_month,
            "expenses_this_week": expenses_this_week,
            "net_this_week": net_this_week,
        })
        return ctx """

from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

from members.models import Member
from groups.models import Group
from visitors.models import Visitor
from services.models import AttendanceRecord
from finance.models import Expense, MeetingCollection
import json


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        today = timezone.localdate()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        total_members = Member.objects.count()
        total_groups = Group.objects.count()
        visitors_this_week = Visitor.objects.filter(date__gte=start_of_week, date__lte=today).count()

        attendance_qs = AttendanceRecord.objects.filter(date__gte=start_of_week, date__lte=today)
        attendance_total = sum(a.total_attendance for a in attendance_qs)

        collections_qs = MeetingCollection.objects.filter(date__gte=start_of_week, date__lte=today)
        collections_this_week = sum((c.total for c in collections_qs), Decimal("0.00"))

        expenses_this_month = (
            Expense.objects
            .filter(date__gte=start_of_month, date__lte=today)
            .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        )

        expenses_this_week = (
            Expense.objects
            .filter(date__gte=start_of_week, date__lte=today)
            .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        )

        net_this_week = collections_this_week - expenses_this_week

        # Last 7 days charts
        last_7_days = [today - timezone.timedelta(days=i) for i in range(6, -1, -1)]
        chart_labels = [d.strftime("%d %b") for d in last_7_days]

        attendance_chart_data = []
        collections_chart_data = []
        expenses_chart_data = []

        for day in last_7_days:
            day_attendance = AttendanceRecord.objects.filter(date=day)
            attendance_chart_data.append(sum(a.total_attendance for a in day_attendance))

            day_collections = MeetingCollection.objects.filter(date=day)
            collections_chart_data.append(float(sum((c.total for c in day_collections), Decimal("0.00"))))

            day_expenses = (
                Expense.objects
                .filter(date=day)
                .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
            )
            expenses_chart_data.append(float(day_expenses))
        recent_members = Member.objects.order_by("-id")[:5]
        recent_visitors = Visitor.objects.order_by("-date")[:5]
        recent_expenses = Expense.objects.order_by("-date")[:5]
        recent_collections = MeetingCollection.objects.order_by("-date")[:5]

        ctx.update({
            """ "today": today,
            "total_members": total_members,
            "total_groups": total_groups,
            "visitors_this_week": visitors_this_week,
            "attendance_this_week": attendance_total,
            "collections_this_week": collections_this_week,
            "expenses_this_month": expenses_this_month,
            "expenses_this_week": expenses_this_week,
            "net_this_week": net_this_week,

            "recent_members": recent_members,
            "recent_visitors": recent_visitors,
            "recent_expenses": recent_expenses,
            "recent_collections": recent_collections,

            "chart_labels": json.dumps(chart_labels),
            "attendance_chart_data": json.dumps(attendance_chart_data),
            "collections_chart_data": json.dumps(collections_chart_data),
            "expenses_chart_data": json.dumps(expenses_chart_data),
              """
            "today": today,
            "total_members": total_members,
            "total_groups": total_groups,
            "visitors_this_week": visitors_this_week,
            "attendance_this_week": attendance_total,
            "collections_this_week": collections_this_week,
            "expenses_this_month": expenses_this_month,
            "expenses_this_week": expenses_this_week,
            "net_this_week": net_this_week,

            "chart_labels": json.dumps(chart_labels),
            "attendance_chart_data": json.dumps(attendance_chart_data),
            "collections_chart_data": json.dumps(collections_chart_data),
            "expenses_chart_data": json.dumps(expenses_chart_data),

            "recent_members": recent_members,
            "recent_visitors": recent_visitors,
            "recent_expenses": recent_expenses,
            "recent_collections": recent_collections,
        })
        return ctx