import os
from django.db import transaction
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movienight.settings')
django.setup()

from django.utils import timezone
from collector.models import Movie, Genre, Actor, Director
from collector.movieInfo import get_movie_details, get_netflix_movies, get_imdb_rating

from django.db import IntegrityError

def convert_youtube_url_to_embed(url):
    if url is not None and "watch?v=" in url:
        return url.replace("watch?v=", "embed/")
    return url

def save_netflix_movies():
    page = 1
    while True:
        movies = get_netflix_movies(page)
        if not movies:
            break

        with transaction.atomic():
            for movie_data in movies:
                movie_details = get_movie_details(movie_data['id'])
                if movie_details:
                    try:
                        release_date = timezone.datetime.strptime(movie_details['release_date'], '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        release_date = None
                        
                    imdb_rating = get_imdb_rating(movie_details['IMDB_id']) if movie_details.get('IMDB_id') else "0"

                    director, _ = Director.objects.get_or_create(
                        Director_id=movie_details.get('director_id'),
                        defaults={
                            'name': movie_details.get('director'),
                            'profile_image': movie_details.get('director_profile')
                        }
                    )

                    converted_trailer_url = convert_youtube_url_to_embed(movie_details['trailer_url'])

                    try:
                        movie, created = Movie.objects.update_or_create(
                            TMDB_id=movie_details['TMDB_id'],
                            defaults={
                                'title': movie_details.get('title'),
                                'director': director,
                                'poster_url': movie_details.get('poster_url'),
                                'release_date': release_date,
                                'popularity': movie_details.get('popularity'),
                                'IMDB_id': movie_details.get('IMDB_id'),
                                'IMDB_rating': imdb_rating,
                                "overview": movie_details.get("overview"),
                                "runtime": movie_details.get("runtime"),
                                'trailer_url': converted_trailer_url, 
                            }
                        )
                    except IntegrityError:
                        print(f"Error saving movie: {movie_details['TMDB_id']}")

                    for genre_name in movie_details['genres']:
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        movie.genres.add(genre)

                    for actor_info in movie_details['lead_actors']:
                        actor, _ = Actor.objects.get_or_create(
                            Actor_id=actor_info.get('id'),
                            defaults={
                                'name': actor_info['name'],
                                'profile_image': actor_info.get('profile_url')
                            }
                        )
                        movie.lead_actors.add(actor)

        page += 1

if __name__ == "__main__":
    save_netflix_movies()
