import requests
import os

Bearer_Token = os.getenv('Authorization') 

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
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&append_to_response=credits"
    headers = {
        "accept": "application/json",
        "Authorization": Bearer_Token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        director_info = next((crew for crew in data.get('credits', {}).get('crew', []) if crew['job'] == 'Director'))
        director_profile = get_person_profile(director_info['id'])

        cast = data.get('credits', {}).get('cast', [])
        lead_actors = sorted(cast, key=lambda actor: actor.get('order', 999))[:3]  
        lead_actors_info = [{"name": actor['name'], "id": actor['id'], "profile_url": get_person_profile(actor['id'])} for actor in lead_actors]

        movie_info = {
            "title": data.get("title"),
            "genres": [genre['name'] for genre in data.get("genres", [])],
            "director": director_info['name'],
            "director_id": director_info['id'],
            "director_profile": director_profile,
            "lead_actors": lead_actors_info,
            "poster_url": f"https://image.tmdb.org/t/p/original{data.get('poster_path')}",
            "release_date": data.get("release_date"),
            "popularity": data.get("popularity"),
            "IMDB_id": data.get("imdb_id"),
            "overview": data.get("overview"),
            "runtime": data.get("runtime"),
            "TMDB_id": data.get("id"),
        }
        
        return movie_info
    else:
        return []

tmdb_id = '787699'
print(get_movie_details(tmdb_id))
