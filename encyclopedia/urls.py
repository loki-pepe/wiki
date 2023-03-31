from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),
]
