from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView

from .models import MeetingCollection, CollectionCategory, CollectionEntry
from .forms import MeetingCollectionForm, CollectionEntryFormSet


class CollectionListView(LoginRequiredMixin, ListView):
    model = MeetingCollection
    template_name = "finance/collections/list.html"
    paginate_by = 25

    def get_queryset(self):
        return (
            MeetingCollection.objects
            .prefetch_related("entries__category")
            .order_by("-date", "-id")
        )


def _ensure_entries_for_all_active_categories(collection: MeetingCollection):
    active = CollectionCategory.objects.filter(is_active=True).order_by("name")
    existing = set(collection.entries.values_list("category_id", flat=True))

    to_create = []
    for cat in active:
        if cat.id not in existing:
            to_create.append(CollectionEntry(collection=collection, category=cat, amount=0))
    if to_create:
        CollectionEntry.objects.bulk_create(to_create)


@transaction.atomic
def collection_create(request):
    if request.method == "POST":
        form = MeetingCollectionForm(request.POST)
        if form.is_valid():
            collection = form.save()
            _ensure_entries_for_all_active_categories(collection)

            formset = CollectionEntryFormSet(request.POST, instance=collection)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Collection saved.")
                return redirect("finance:collections_list")
        else:
            formset = CollectionEntryFormSet(request.POST)
    else:
        form = MeetingCollectionForm()
        formset = None

    active_categories = CollectionCategory.objects.filter(is_active=True).order_by("name")
    return render(request, "finance/collections/form.html", {
        "form": form,
        "formset": formset,
        "active_categories": active_categories,
        "title": "New Meeting Collection",
        "cancel_url": reverse_lazy("finance:collections_list"),
        "is_create": True,
    })


@transaction.atomic
def collection_update(request, pk):
    collection = get_object_or_404(MeetingCollection, pk=pk)
    _ensure_entries_for_all_active_categories(collection)

    if request.method == "POST":
        form = MeetingCollectionForm(request.POST, instance=collection)
        formset = CollectionEntryFormSet(request.POST, instance=collection)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Collection updated.")
            return redirect("finance:collections_list")
    else:
        form = MeetingCollectionForm(instance=collection)
        formset = CollectionEntryFormSet(instance=collection)

    return render(request, "finance/collections/form.html", {
        "form": form,
        "formset": formset,
        "title": "Edit Meeting Collection",
        "cancel_url": reverse("finance:collections_list"),
        "is_create": False,
    })