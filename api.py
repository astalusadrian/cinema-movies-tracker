from config import ENDPOINTS, get_cinemas_json_path, get_cinemas_folder_path
from datetime import datetime
from pathlib import Path
import requests
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
    
class MoviesAPI:
    def __init__(self):
        self._endpoints = ENDPOINTS

    def _api_call(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            print("API call successful.")
            return response.json()
        except requests.RequestException as e:
            print(f"API call failed: {e}")
            return None

    def _read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File '{path}' not found.")
            return None

    def _write_file(self, data, path):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Failed to write to file '{path}': {e}")

    def _get_movies_from_section(self, section):
        url = self._endpoints.get(section)
        if not url:
            print(f"Endpoint for section '{section}' not found.")
            return None

        response = self._api_call(url)
        if response is None:
            print(f"Failed to retrieve data for section '{section}'.")
            return None

        return response.get('body', {}).get('posters', [])

    def get_coming_soon_movies(self):
        return self._get_movies_from_section("coming_soon")

    def get_now_playing_movies(self):
        return self._get_movies_from_section("now_playing")
    
    def get_movies_list(self):

        movies_by_code = {} # Dictionary to hold movies data by their unique code
        
        # Tuple of fields to extract for each movie entry
        movie_fields = (
            "code",
            "attributes",
            "featureTitle",
            "url",
            "dateStarted",
            "filmShowingType"
        )

        # Loop through each section to retrieve movies and organize them by their code
        for section, movies in (
            ("coming_soon", self.get_coming_soon_movies()),
            ("now_playing", self.get_now_playing_movies())
        ):
            # Check if the movies were retrieved successfully
            if movies is None:
                print(f"Skipping section '{section}' due to previous errors.")
                continue

            # Parse each movie of the section
            for movie in movies:
                movie_code = movie.get('code')
                if not movie_code: 
                    continue  # Skip if 'code' is missing

                # Extract relevant fields for the movie
                movie_details = {
                    key: movie[key]
                    for key in movie_fields
                    if key in movie
                }

                # Add movie details to the dictionary of movies, skipping duplicates
                entry = movies_by_code.setdefault(movie_code, {**movie_details,  "sections": []})
                entry["sections"].append(section) # Add the section where the movie was found

        return movies_by_code


    '''
    def get_cinemas(self):
        if self.already_has_snapshot_for_today():
            print("Snapshot for today already exists. Skipping API call.")
            return
        cinemas_data_raw = self.api_call(self._cinemas_url)
        cinemas_data_final = {}
        if cinemas_data_raw:
            cinemas_data = cinemas_data_raw.get('body',{}).get('cinemas', [])
            if not cinemas_data:
                print("No cinemas data found in the API response.")
                return None
            
            for cinema_data in cinemas_data:
                cinema_id  = str(cinema_data.get('id'))
                cinemas_data_final[cinema_id] = {
                    'groupId': cinema_data.get('groupId'),
                    'displayName': cinema_data.get('displayName'),
                    'link': cinema_data.get('link'),
                    'imageUrl': cinema_data.get('imageUrl'),
                    'address': cinema_data.get('addressInfo', {}).get('address1', ''),
                    'city': cinema_data.get('addressInfo', {}).get('city', ''),
                    'latitude': cinema_data.get('latitude'),
                    'longitude': cinema_data.get('longitude'),
                }

            self.create_cinemas_snapshot(cinemas_data_final)
    '''
    def get_cinemas(self):
        print("Retrieving cinemas data...")
        


    def run(self):
        print('Retrieving cinemas data...')
        self.get_cinemas()
