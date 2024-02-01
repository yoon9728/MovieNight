import requests
import os
from bs4 import BeautifulSoup

Bearer_Token = os.getenv('Authorization') 

def get_netflix_movies(page=1):
    netflix_provider_id = 8  
    url = f"https://api.themoviedb.org/3/discover/movie?with_watch_providers={netflix_provider_id}&watch_region=CA&page={page}&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": Bearer_Token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Error: {response.status_code}")
        return []

def get_person_profile(person_id):
    url = f"https://api.themoviedb.org/3/person/{person_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": Bearer_Token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        profile_path = data.get('profile_path')
        if profile_path:
            return f"https://image.tmdb.org/t/p/original{profile_path}"
        else:
            return None
    else:
        return None

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&append_to_response=videos,credits"
    headers = {
        "accept": "application/json",
        "Authorization": Bearer_Token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        director_info = next((crew for crew in data.get('credits', {}).get('crew', []) if crew['job'] == 'Director'), None)
        if director_info:
            director_profile = get_person_profile(director_info['id'])
        else:
            director_profile = None

        cast = data.get('credits', {}).get('cast', [])
        lead_actors = sorted(cast, key=lambda actor: actor.get('order', 999))[:3]
        lead_actors_info = [{"name": actor['name'], "id": actor['id'], "profile_url": get_person_profile(actor['id'])} for actor in lead_actors]

        trailers = data.get('videos', {}).get('results', [])
        if trailers:
            youtube_trailer_url = next((f"https://www.youtube.com/watch?v={trailer['key']}" for trailer in trailers if trailer['site'] == 'YouTube' and trailer['type'] == 'Trailer'), None)
        else:
            youtube_trailer_url = None

        movie_info = {
            "title": data.get("title"),
            "genres": [genre['name'] for genre in data.get("genres", [])],
            "director": director_info['name'] if director_info else None,
            "director_id": director_info['id'] if director_info else None,
            "director_profile": director_profile,
            "lead_actors": lead_actors_info,
            "poster_url": f"https://image.tmdb.org/t/p/original{data.get('poster_path')}",
            "release_date": data.get("release_date"),
            "popularity": data.get("popularity"),
            "IMDB_id": data.get("imdb_id"),
            "overview": data.get("overview"),
            "runtime": data.get("runtime"),
            "TMDB_id": data.get("id"),
            "trailer_url": youtube_trailer_url, 
        }
        
        return movie_info
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return []

def get_imdb_rating(imdb_id):
    url = f'https://www.imdb.com/title/{imdb_id}/'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    rating_span = soup.find('span', {'class': 'sc-bde20123-1 cMEQkK'}) 
    if rating_span is not None:
        return rating_span.text
    else:
        return None