from django.urls import path
from .views import VisitorListView, VisitorCreateView, VisitorUpdateView

app_name = "visitors"

urlpatterns = [
    path("", VisitorListView.as_view(), name="list"),
    path("new/", VisitorCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", VisitorUpdateView.as_view(), name="update"),
]
