
from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_events, name="upload_events"),
]
