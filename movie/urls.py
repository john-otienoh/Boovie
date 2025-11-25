from django.urls import path
from .views import home, detail, search

app_name = "movie"

urlpatterns = [

    path("", home, name="home"),
    path("search/", search, name="search"),
    path("<slug:slug>/", detail, name="detail"),
   
]
