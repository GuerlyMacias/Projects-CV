from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logoutV,name="logoutV"),
    path("home",views.home,name="home"),
    path("createusers",views.createusers,name="createusers"),
    path("lessons", views.lessons, name="lessons"),
    path("pruebas",views.pruebas,name = "pruebas"),
    path("options",views.options,name = "options"),

]