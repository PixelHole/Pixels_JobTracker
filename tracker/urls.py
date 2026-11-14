from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ApplicationListView.as_view(), name="application-list"),
    path("applications/new/", views.ApplicationCreateView.as_view(), name="application-create"),
    path("applications/<int:pk>/edit/", views.ApplicationUpdateView.as_view(), name="application-update"),
    path("applications/<int:pk>/delete/", views.ApplicationDeleteView.as_view(), name="application-delete"),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]
