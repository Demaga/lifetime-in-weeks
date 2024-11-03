from django.urls import path

from . import views

app_name = "lifetime"
urlpatterns = [
    path("", views.index, name="index"),
]
