from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Movie

# Create your views here.

def detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    return render(request, "movie/detail.html", {"movie": movie})

def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        movie_results = Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return render(
            request, "movie/search.html", {"query": query, "movies": movie_results}
        )
    return render(request, "movie/search.html")


def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {"movies": movies})
