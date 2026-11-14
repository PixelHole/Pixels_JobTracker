from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import FormView

from .forms import ApplicationForm
from .models import Application


class SignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("application-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserApplicationsMixin(LoginRequiredMixin):
    """Restrict every query to the logged-in user's own applications."""

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)


class ApplicationListView(UserApplicationsMixin, ListView):
    template_name = "tracker/application_list.html"
    context_object_name = "applications"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status", "")
        query = self.request.GET.get("q", "").strip()
        if status in Application.Status.values:
            qs = qs.filter(status=status)
        if query:
            qs = qs.filter(
                Q(company__icontains=query) | Q(position__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # One aggregate query for the dashboard counts, over all of the user's data.
        counts = dict(
            super()
            .get_queryset()
            .values_list("status")
            .annotate(total=Count("id"))
            .order_by()
        )
        context["stats"] = [
            (value, label, counts.get(value, 0))
            for value, label in Application.Status.choices
        ]
        context["total"] = sum(counts.values())
        context["statuses"] = Application.Status.choices
        context["current_status"] = self.request.GET.get("status", "")
        context["query"] = self.request.GET.get("q", "")
        return context


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "tracker/application_form.html"
    success_url = reverse_lazy("application-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Application added.")
        return super().form_valid(form)


class ApplicationUpdateView(UserApplicationsMixin, UpdateView):
    form_class = ApplicationForm
    template_name = "tracker/application_form.html"
    success_url = reverse_lazy("application-list")

    def form_valid(self, form):
        messages.success(self.request, "Application updated.")
        return super().form_valid(form)


class ApplicationDeleteView(UserApplicationsMixin, DeleteView):
    template_name = "tracker/application_confirm_delete.html"
    success_url = reverse_lazy("application-list")

    def form_valid(self, form):
        messages.success(self.request, "Application deleted.")
        return super().form_valid(form)
