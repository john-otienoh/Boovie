from django.urls import path
from .views import list, detail, search

app_name = "movie"

urlpatterns = [
    path("", list, name="list"),
    path("<slug:post>/", detail, name="detail"),
    path("search/", search, name="search"),
]
