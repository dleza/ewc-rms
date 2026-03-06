from django.urls import path
from .views import (
    GroupListView, GroupCreateView, GroupUpdateView, GroupDetailView,
    update_group_members
)

app_name = "groups"

urlpatterns = [
    path("", GroupListView.as_view(), name="list"),
    path("new/", GroupCreateView.as_view(), name="create"),
    path("<int:pk>/", GroupDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", GroupUpdateView.as_view(), name="update"),
    path("<int:pk>/members/update/", update_group_members, name="members_update"),
]
