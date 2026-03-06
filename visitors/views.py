from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Visitor
from .forms import VisitorForm


class VisitorListView(LoginRequiredMixin, ListView):
    model = Visitor
    template_name = "visitors/visitor_list.html"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().order_by("-date", "-id")
        q = self.request.GET.get("q")
        need_visitation = self.request.GET.get("need_visitation")
        joining = self.request.GET.get("joining")
        born_again = self.request.GET.get("born_again")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        if q:
            qs = qs.filter(
                Q(full_name__icontains=q) |
                Q(address__icontains=q) |
                Q(phone1__icontains=q) |
                Q(phone2__icontains=q) |
                Q(prayer_request__icontains=q)
            )

        # boolean filters come as strings: "1" or "" (or None)
        if need_visitation == "1":
            qs = qs.filter(need_visitation=True)
        if joining == "1":
            qs = qs.filter(joining=True)
        if born_again == "1":
            qs = qs.filter(born_again=True)

        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)

        return qs


class VisitorCreateView(CreateView):
    model = Visitor
    form_class = VisitorForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("visitors:list")

    def form_valid(self, form):
        messages.success(self.request, "Visitor saved.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "New Visitor"
        ctx["cancel_url"] = reverse_lazy("visitors:list")
        return ctx


class VisitorUpdateView(UpdateView):
    model = Visitor
    form_class = VisitorForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("visitors:list")

    def form_valid(self, form):
        messages.success(self.request, "Visitor updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Edit Visitor"
        ctx["cancel_url"] = reverse_lazy("visitors:list")
        return ctx
