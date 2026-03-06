from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Member
from .forms import MemberForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    paginate_by = 20
    template_name = "members/member_list.html"

    def get_queryset(self):
        qs = super().get_queryset().order_by("full_name")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(member_no__icontains=q) |
                Q(full_name__icontains=q) |
                Q(phone1__icontains=q) |
                Q(phone2__icontains=q) |
                Q(email__icontains=q)
            )
        return qs
class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("members:list")

    def form_valid(self, form):
        messages.success(self.request, "Member saved successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "New Member"
        ctx["cancel_url"] = reverse_lazy("members:list")
        return ctx

class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("members:list")

    def form_valid(self, form):
        messages.success(self.request, "Member updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Edit Member"
        ctx["cancel_url"] = reverse_lazy("members:list")
        return ctx

class MemberDetailView(DetailView):
    model = Member
    template_name = "members/member_detail.html"
