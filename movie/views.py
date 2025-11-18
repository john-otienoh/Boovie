from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Movie

# Create your views here.
def list(request):
    movies = Movie.objects.all()
    return render(request, 'list.html', {"movies": movies})

def detail(request):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "detail.html", {"movie": movie})

def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        movie_results = Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return render(
            request, "search.html", {"query": query, "movie_results": movie_results}
        )
    return render(request, "search.html")
