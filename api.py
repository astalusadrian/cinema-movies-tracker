from endpoints import CINEMAS_URL, MOVIES_IN_CINEMA_URL, get_cinemas_json_path, get_cinemas_folder_path
from datetime import datetime
from pathlib import Path
import requests
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
    
class MoviesAPI:
    def __init__(self):
        self._cinemas_url = CINEMAS_URL
        self._movies_in_cinema_url = MOVIES_IN_CINEMA_URL

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

    def create_cinemas_snapshot(self, cinemas_data):
        print("Creating a snapshot of the cinemas data...")
        snapshot_path = get_cinemas_json_path()
        self.write_file(cinemas_data, snapshot_path)
        print(f"Cinemas snapshot created at '{snapshot_path}'.")

    def already_has_snapshot_for_today(self):
        todays_date = datetime.now().strftime("%Y-%m-%d")
        folder = Path(get_cinemas_folder_path())
        for file in folder.glob("cinemas_*.json"):
            if todays_date in file.name:
                return True
        return False

    def api_call(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            print("API call successful.")
            return response.json()
        except requests.RequestException as e:
            print(f"API call failed: {e}")
            return None
        
    def read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File '{path}' not found.")
            return None

    def write_file(self, data, path):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Failed to write to file '{path}': {e}")

    def run(self):
        print('Retrieving cinemas data...')
        self.get_cinemas()
