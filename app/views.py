from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import PersonalRecord
from django.contrib.auth.forms import UserCreationForm
from .forms import PersonalRecordForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirige vers /accounts/login/
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

class PRListView(LoginRequiredMixin, ListView):
    model = PersonalRecord
    template_name = "records/pr_list.html"
    context_object_name = "records"

    def get_queryset(self):
        queryset = PersonalRecord.objects.filter(user=self.request.user)

        # Filtrage par exercice sélectionné
        selected_exercise = self.request.GET.get("exercise", "")
        if selected_exercise:
            queryset = queryset.filter(title=selected_exercise)

        return queryset.order_by("-date")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Liste unique des exercices de l'utilisateur
        exercises = PersonalRecord.objects.filter(user=self.request.user).values_list("title", flat=True).distinct()
        context["exercises"] = exercises
        context["selected_exercise"] = self.request.GET.get("exercise", "")
        
        return context

class PRCreateView(LoginRequiredMixin, CreateView):
    model = PersonalRecord
    form_class = PersonalRecordForm
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
    
class PRDetailView(LoginRequiredMixin, DetailView):
    model = PersonalRecord
    template_name = "records/pr_detail.html"
    context_object_name = "object"

    def get_queryset(self):
        return PersonalRecord.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = PersonalRecord.objects.filter(
            user=self.request.user,
            title=self.object.title
        ).order_by("date")
        context["dates"] = [str(pr.date) for pr in qs]
        context["values"] = [pr.value for pr in qs]
        context["records"] = qs
        return context
    