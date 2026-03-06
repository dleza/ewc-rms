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


""" from django.contrib import admin
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
] """

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import DashboardView
from accounts.forms import BootstrapPasswordResetForm, BootstrapSetPasswordForm
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),

    path("members/", include("members.urls")),
    path("groups/", include("groups.urls")),
    path("attendance/", include("services.urls")),
    path("visitors/", include("visitors.urls")),
    path("finance/", include("finance.urls")),

    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    path(
    "accounts/password_reset/",
    auth_views.PasswordResetView.as_view(
        form_class=BootstrapPasswordResetForm,
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
        success_url="/accounts/password_reset/done/",
    ),
    name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
    "accounts/reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        form_class=BootstrapSetPasswordForm,
        template_name="registration/password_reset_confirm.html",
        success_url="/accounts/reset/done/",
    ),
    name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]