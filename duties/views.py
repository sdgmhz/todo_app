from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from .models import Duty
from accounts.models import Profile


class DutyListView(LoginRequiredMixin, ListView):
    model = Duty
    template_name = "duties/duty_list.html"
    paginate_by = 3
    context_object_name = "duties"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Duty.objects.filter(author=profile).order_by("-updated_date")


class DutyDetailView(LoginRequiredMixin, DetailView):
    model = Duty
    template_name = "duties/duty_detail.html"
    context_object_name = "duty"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Duty.objects.filter(author=profile)


class DutyCreateView(LoginRequiredMixin, CreateView):
    model = Duty
    fields = ("title", "description", "done_status", "deadline_date")
    template_name = "duties/duty_update_create.html"
    success_url = reverse_lazy("duty_list")

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = profile
        return super().form_valid(form)


class DutyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Duty
    fields = ("title", "description", "done_status", "deadline_date")
    template_name = "duties/duty_update_create.html"
    success_url = reverse_lazy("duty_list")

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = profile
        return super().form_valid(form)

    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().author == profile


class DutyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Duty
    template_name = "duties/duty_delete.html"
    success_url = reverse_lazy("duty_list")

    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().author == profile


class ChangeStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Duty, pk=pk)

    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().author == profile

    def post(self, request, pk, *args, **kwargs):
        duty = get_object_or_404(Duty, pk=pk)
        profile = get_object_or_404(Profile, user=self.request.user)
        if duty.author != profile:
            return HttpResponseRedirect(reverse("403"))
        if duty.done_status == "not":
            duty.done_status = "don"
        else:
            duty.done_status = "not"
        duty.save(update_fields=["done_status"])

        return HttpResponseRedirect(reverse("duty_list"))
