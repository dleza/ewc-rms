from django.urls import path
from .views import MemberListView, MemberCreateView, MemberUpdateView, MemberDetailView

app_name = "members"
urlpatterns = [
    path("", MemberListView.as_view(), name="list"),
    path("new/", MemberCreateView.as_view(), name="create"),
    path("<int:pk>/", MemberDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", MemberUpdateView.as_view(), name="update"),
]
