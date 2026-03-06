from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import AttendanceRecord, ActivityType
from .forms import AttendanceForm
from groups.models import Group


class AttendanceListView(LoginRequiredMixin, ListView):
    model = AttendanceRecord
    template_name = "services/attendance_list.html"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related("group").order_by("-date", "-id")
        q = self.request.GET.get("q")
        activity = self.request.GET.get("activity")
        group_id = self.request.GET.get("group")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        if q:
            qs = qs.filter(
                Q(preacher__icontains=q) |
                Q(title_of_msg__icontains=q) |
                Q(group__name__icontains=q)
            )
        if activity:
            qs = qs.filter(activity_type=activity)
        if group_id:
            qs = qs.filter(group_id=group_id)
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["groups"] = Group.objects.all().order_by("group_type", "name")
        ctx["activities"] = ActivityType.choices

        # totals for filtered queryset
        qs = self.get_queryset()
        totals = qs.aggregate(
            af=Sum("adult_female"), am=Sum("adult_male"),
            tf=Sum("teen_female"), tm=Sum("teen_male"),
            cf=Sum("children_female"), cm=Sum("children_male"),
        )
        ctx["totals"] = {k: (v or 0) for k, v in totals.items()}
        ctx["grand_total"] = sum(ctx["totals"].values())
        return ctx


class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = AttendanceRecord
    form_class = AttendanceForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("services:attendance_list")

    def form_valid(self, form):
        messages.success(self.request, "Attendance record saved.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "New Attendance Record"
        ctx["cancel_url"] = reverse_lazy("services:attendance_list")
        return ctx


class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = AttendanceRecord
    form_class = AttendanceForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("services:attendance_list")

    def form_valid(self, form):
        messages.success(self.request, "Attendance record updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Edit Attendance Record"
        ctx["cancel_url"] = reverse_lazy("services:attendance_list")
        return ctx
