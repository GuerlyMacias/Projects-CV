from django.urls import path

from . import views


app_name="entries"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search/<str:q>/",views.search, name="search"),
    path("apology/<str:info>/",views.apology,name="apology"),
    path("create/", views.create, name="create"),
    path("edit/",views.edit,name="edit"),
    path("random_page/",views.random_page,name="random_page")
]
