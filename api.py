from endpoints import CINEMAS_URL, MOVIES_IN_CINEMA_URL
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')
    
class MoviesAPI:
    def __init__(self):
        self._cinemas_url = CINEMAS_URL
        self._movies_in_cinema_url = MOVIES_IN_CINEMA_URL
        self._cinemas_cache = {}
        
        self._set_cinemas_cache()

    def _set_cinemas_cache(self):
        cinemas = self.api_call(self._cinemas_url)
        if not cinemas:
            raise ValueError("Failed to retrieve cinemas for caching.")
        cinema_list = cinemas['body']['cinemas']
        for cinema in cinema_list:
            self._cinemas_cache[cinema['displayName']] = {'id': cinema['id']}
            # In the future maybe add more details to the cache, like location, address, etc.

    def get_cinemas_cache(self):
        return self._cinemas_cache

    def api_call(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API call failed: {e}")
            return None
        
    def get_cinemas(self):
        return self.api_call(self._cinemas_url)

    def get_cinema_id_by_name(self, cinema_name):
        return self._cinemas_cache.get(cinema_name, {}).get('id')

    def get_movies_data_raw(self, cinema_name):
        cinema_id = self.get_cinema_id_by_name(cinema_name)
        if not cinema_id:
            print(f"Cinema '{cinema_name}' not found in cache.")
            return None

        url = self._movies_in_cinema_url.format(cinema_id=cinema_id)
        return self.api_call(url)
    
    def get_movies_in_cinema(self, cinema_name):
        movies_data = self.get_movies_data_raw(cinema_name)
        if not movies_data:
            return None
        
        films = movies_data['body']['films']
        for film in films:
            print(f"Title: {film['name']}")
            print(f"Release Year: {film['releaseYear']}")
            print(f"Duration: {film['length']} minutes")
            print(f"Genres: {', '.join(film['attributeIds'])}")
            print("-" * 40)

