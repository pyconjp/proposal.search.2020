from django.urls import path

from . import views


app_name = "search"
urlpatterns = [
    path("talk/", views.list_talks, name="list_talks"),
]
