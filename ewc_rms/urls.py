"""
URL configuration for ewc_rms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
""" from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="members:list", permanent=False)),
    path("admin/", admin.site.urls),

    path("members/", include("members.urls")),
    path("groups/", include("groups.urls")),
    path("attendance/", include("services.urls")),
    path("visitors/", include("visitors.urls")),
    path("finance/", include("finance.urls")),
    

   
      # ✅ Login/Logout/Password reset (Django built-in)
    path("accounts/", include("django.contrib.auth.urls")),

    # optional: home redirect
    path("", RedirectView.as_view(pattern_name="members:list", permanent=False)),
] """


from django.contrib import admin
from django.urls import path, include
from core.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),

    path("members/", include("members.urls")),
    path("groups/", include("groups.urls")),
    path("attendance/", include("services.urls")),
    path("visitors/", include("visitors.urls")),
    path("finance/", include("finance.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

