from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("records/", views.record_list, name="record_list"),
]