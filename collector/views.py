from django.views.generic import ListView
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from .models import Movie, Genre, Actor
from .movieInfo import get_netflix_movies, get_movie_details
from django.http import JsonResponse
from django.db.models import Q
import random


class HomePage(ListView):
    template_name = 'movienight/homepage.html'
    context_object_name = 'movies'
    paginate_by = 21
    

    def get_queryset(self):
        # 데이터베이스에 영화가 없는 경우, 영화 정보를 불러와 저장
        if not Movie.objects.exists():
            for page in range(1, 3):
                for movie_data in get_netflix_movies(page):
                    movie_details = get_movie_details(movie_data['id'])
                    movie, created = Movie.objects.update_or_create(
                        title=movie_details['title'],
                        defaults={
                            'director': movie_details['director'],
                            'poster_url': movie_details['poster_url'],
                        }
                    )
                    movie.genres.clear()
                    for genre_name in movie_details['genres']:
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        movie.genres.add(genre)

        # 정렬 쿼리 파라미터 처리
        sort = self.request.GET.get('sort', '')
        if sort == 'Title':
            queryset = Movie.objects.all().order_by('title')
        elif sort == 'Release_date':
            queryset = Movie.objects.all().order_by('-release_date')
        elif sort == 'Popularity':
            queryset = Movie.objects.all().order_by('-popularity')
        elif sort == 'rating':
            queryset = Movie.objects.all().order_by('-IMDB_rating')
        else:
            queryset = Movie.objects.all().order_by('-popularity')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['actors'] = Actor.objects.all()
        return context
    
def load_movies(request):
    page_number = request.GET.get('page', 1)
    genres_param = request.GET.get('genres', '')
    sort = request.GET.get('sort', 'default')
    search_query = request.GET.get('search', '')
    genres = genres_param.split(',') if genres_param else []

    movies_query = Movie.objects.all()

    if search_query:
        movies_query = movies_query.filter(title__icontains=search_query)

    if genres:
        query = Q(genres__name=genres[0])
        for genre in genres[1:]:
            query |= Q(genres__name=genre)
        movies_query = movies_query.filter(query).distinct()

    if sort == 'Title':
        movies_query = movies_query.order_by('title')
    elif sort == 'Release_date':
        movies_query = movies_query.order_by('-release_date')
    elif sort == 'Popularity':
        movies_query = movies_query.order_by('-popularity')
    elif sort == 'rating':
        movies_query = movies_query.order_by('-IMDB_rating')

    paginator = Paginator(movies_query, 21)
    page_obj = paginator.get_page(page_number)

    movie_data = [
        {
            'title': movie.title,
            'genres': [genre.name for genre in movie.genres.all()],
            'poster_url': movie.poster_url,
            'IMDB_rating': movie.IMDB_rating,
            'release_date': movie.release_date,
            'TMDB_id': movie.TMDB_id,
        } for movie in page_obj
    ]

    return JsonResponse({
        'movies': movie_data,
        'has_next': page_obj.has_next(),
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    })



def load_more_movies(request):
    page = request.GET.get('page')
    genres = request.GET.getlist('genres')

    movies_query = Movie.objects.all()

    if genres:
        # 선택한 장르 중 하나라도 만족하는 영화 필터링
        selected_movies = []
        for movie in movies_query:
            for genre in genres:
                if genre in [genre.name for genre in movie.genres.all()]:
                    selected_movies.append(movie)
                    break
        movies_query = selected_movies

    movies = movies_query[(int(page) - 1) * 21:int(page) * 21]

    movie_data = []

    for movie in movies:
        movie_data.append({
            'title': movie.title,
            'genres': [genre.name for genre in movie.genres.all()],
            'poster_url': movie.poster_url,
            'IMDB_rating': movie.IMDB_rating,
            'release_date': movie.release_date, 
            'TMDB_id': movie.TMDB_id,

        })

    return JsonResponse({'movies': movie_data})

class todaysPick(ListView):
    model = Movie
    template_name = 'movienight/todaysPick.html'
    context_object_name = 'movies'
    queryset = Movie.objects.order_by('-popularity')[:50]

    def get_queryset(self):
        top_movies = list(self.queryset) 
        random_movies = random.sample(top_movies, 3)  
        return random_movies

class About(TemplateView):
    template_name = "movienight/about.html"
