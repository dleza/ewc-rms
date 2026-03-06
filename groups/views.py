from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from members.models import Member
from .models import Group, GroupType
from .forms import GroupForm, GroupMembersForm


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("leader").prefetch_related("members")
        q = self.request.GET.get("q")
        gtype = self.request.GET.get("type")

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(leader__full_name__icontains=q))
        if gtype in (GroupType.MINISTRY, GroupType.SERVICE):
            qs = qs.filter(group_type=gtype)

        return qs.order_by("group_type", "name")


class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("groups:list")

    def form_valid(self, form):
        messages.success(self.request, "Group created.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "New Group"
        ctx["cancel_url"] = reverse_lazy("groups:list")
        return ctx


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "generic/form.html"

    def get_success_url(self):
        return reverse("groups:detail", args=[self.object.id])

    def form_valid(self, form):
        messages.success(self.request, "Group updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Edit Group"
        ctx["cancel_url"] = reverse("groups:detail", args=[self.object.id])
        return ctx


class GroupDetailView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Member search inside assignment page
        member_q = self.request.GET.get("member_q")
        member_qs = Member.objects.all().order_by("full_name")
        if member_q:
            member_qs = member_qs.filter(
                Q(full_name__icontains=member_q) |
                Q(member_no__icontains=member_q) |
                Q(phone1__icontains=member_q)
            )

        # Pre-select current members
        form = GroupMembersForm(
            member_qs=member_qs,
            initial={"members": self.object.members.all()}
        )

        ctx["members_form"] = form
        ctx["member_q"] = member_q or ""
        return ctx


def update_group_members(request, pk):
    group = get_object_or_404(Group, pk=pk)

    member_q = request.GET.get("member_q")  # preserve filter
    member_qs = Member.objects.all().order_by("full_name")
    if member_q:
        member_qs = member_qs.filter(
            Q(full_name__icontains=member_q) |
            Q(member_no__icontains=member_q) |
            Q(phone1__icontains=member_q)
        )

    if request.method != "POST":
        return redirect("groups:detail", pk=group.pk)

    form = GroupMembersForm(request.POST, member_qs=member_qs)
    if form.is_valid():
        # IMPORTANT: set members from ALL members queryset, not only filtered ones:
        # We want the POST list to be the definitive selection.
        selected_members = form.cleaned_data["members"]
        group.members.set(selected_members)
        messages.success(request, "Group members updated.")
    else:
        messages.error(request, "Please correct the errors and try again.")

    url = reverse("groups:detail", args=[group.pk])
    if member_q:
        url += f"?member_q={member_q}"
    return redirect(url)
