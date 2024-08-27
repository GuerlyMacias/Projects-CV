from . import views
from django.urls import path



urlpatterns = [
    path("", views.loginV,name = "loginV"),
    path("index",views.index,name= "index"),
    path("logoutV",views.logoutV,name="logoutV"),
    path("create",views.create, name="create"),
    path("guardados",views.guardados,name="guardados"),
    path("registro",views.registro,name="registro"),


]