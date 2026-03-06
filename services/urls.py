from django.urls import path
from .views import AttendanceListView, AttendanceCreateView, AttendanceUpdateView

app_name = "services"

urlpatterns = [
    path("", AttendanceListView.as_view(), name="attendance_list"),
    path("new/", AttendanceCreateView.as_view(), name="attendance_create"),
    path("<int:pk>/edit/", AttendanceUpdateView.as_view(), name="attendance_update"),
]
