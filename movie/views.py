from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Genre, Movie

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
        paginator = Paginator(movie_results, 6)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context = {
            'query': query,
            'page_obj': page_obj,
        }
        return render(request, "movie/search.html", context)
    
    return render(request, "movie/search.html")


def home(request):
    status = request.GET.get('status')
    genre_id = request.GET.get('genre')
    language = request.GET.get('language')
    age_rating = request.GET.get('age_rating')

    movies = Movie.objects.all()
    if status:
        movies = movies.filter(status=status)
    if genre_id:
        movies = movies.filter(genre__id=genre_id)
    if language:
        movies = movies.filter(language__iexact=language)
    if age_rating:
        movies = movies.filter(age_rating=age_rating)

    sort_by = request.GET.get('sort_by')
    if sort_by == 'title_asc':
        movies = movies.order_by('title')
    elif sort_by == 'title_desc':
        movies = movies.order_by('-title')
    elif sort_by == 'release_asc':
        movies = movies.order_by('release_date')
    elif sort_by == 'release_desc':
        movies = movies.order_by('-release_date')
    elif sort_by == 'duration_asc':
        movies = movies.order_by('duration')
    elif sort_by == 'duration_desc':
        movies = movies.order_by('-duration')
    else:
        movies = movies.order_by('-created_at') 

    genres = Genre.objects.all()
    languages = Movie.objects.values_list('language', flat=True).distinct()
    age_ratings = [choice[0] for choice in Movie.AGE_RATINGS]
    statuses = [choice[0] for choice in Movie.STATUS_CHOICES]

    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        # 'movies': movies,
        'genres': genres,
        'languages': languages,
        'age_ratings': age_ratings,
        'statuses': statuses,
        'selected_status': status or '',
        'selected_genre': genres or '',
        'selected_language': language or '',
        'selected_age_rating': age_rating or '',
        'selected_sort': sort_by or '',
        'page_obj': page_obj,
        'paginator': paginator,
        'query_params': request.GET.copy(),
    }

    return render(request, 'home.html', context)
