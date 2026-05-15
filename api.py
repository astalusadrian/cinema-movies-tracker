from endpoints import CINEMAS_URL, MOVIES_IN_CINEMA_URL, CINEMAS_JSON_PATH
import requests
import sys
import json
sys.stdout.reconfigure(encoding='utf-8')
    
class MoviesAPI:
    def __init__(self):
        self._cinemas_url = CINEMAS_URL
        self._movies_in_cinema_url = MOVIES_IN_CINEMA_URL
        self._cinemas_path = CINEMAS_JSON_PATH
        self._cinemas_cache = {}

        self._set_cinemas_cache()

    def _set_cinemas_cache(self):

        file_data = self.read_file(self._cinemas_path)
        if not file_data:
            print("No cinema cache found. Fetching from API...")
            api_cinema_data = self.api_call(self._cinemas_url)
            self._build_cinemas_cache(api_cinema_data)
            self.write_file(self._cinemas_cache, self._cinemas_path)
        else:
            print("Cinema cache loaded from file.")
            self._cinemas_cache = file_data

    def _build_cinemas_cache(self, cinema_data):
        if not cinema_data:
            raise ValueError("No cinema data provided to build cache.")
        
        for cinema in cinema_data['body']['cinemas']:
            self._cinemas_cache[cinema['displayName']] = {
                'id': cinema['id']}



    def api_call(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API call failed: {e}")
            return None
        
    def read_file(self, path):
        print(f"Reading file from '{path}'...")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File '{path}' not found.")
            return None

    def write_file(self, data, path):

        print(f"Writing file to '{path}'...")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Failed to write to file '{path}': {e}")


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

