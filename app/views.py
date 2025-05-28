from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import PersonalRecord

# Create your views here.

class PRListView(LoginRequiredMixin, ListView):
    model = PersonalRecord
    template_name = "records/pr_list.html"
    context_object_name = "records"

    def get_queryset(self):
        return PersonalRecord.objects.filter(user=self.request.user)

class PRCreateView(LoginRequiredMixin, CreateView):
    model = PersonalRecord
    fields = ["title", "value", "unit"]
    template_name = "records/pr_form.html"
    success_url = reverse_lazy("pr-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PRDeleteView(LoginRequiredMixin, DeleteView):
    model = PersonalRecord
    template_name = "records/pr_confirm_delete.html"
    success_url = reverse_lazy("pr-list")

    def get_queryset(self):
        return PersonalRecord.objects.filter(user=self.request.user)