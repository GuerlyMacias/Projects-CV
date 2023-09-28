
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creator", views.creator, name="creator"),
    path("liker/<int:code>",views.liker,name="liker"),
    path("editer/<int:code>", views.editer, name="editer"),
    path("profile/<str:code>",views.profile,name="profile"),
    path("profile/follow/<str:code>",views.follow,name="follow"),
    path("followp",views.followp,name="followp"),
    path("profile/liker/<int:code>",views.liker,name="liker"),
    path("profile/editer/<int:code>", views.editer, name="editer"),
]
