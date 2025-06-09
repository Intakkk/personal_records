from django.urls import path
from .views import PRListView, PRCreateView, PRDeleteView, PRDetailView
# Define URL patterns for the app

urlpatterns = [
    path("", PRListView.as_view(), name="pr-list"),
    path("add/", PRCreateView.as_view(), name="pr-add"),
    path("delete/<int:pk>/", PRDeleteView.as_view(), name="pr-delete"),
    path("pr/<int:pk>/", PRDetailView.as_view(), name="pr-detail"),
]