from datetime import datetime
from pathlib import Path

ENDPOINTS = {
    "coming_soon": "https://www.cinemacity.ro/ro/data-api-service/v1/feed/10107/byName/coming-soon?lang=ro_RO",
    "now_playing": "https://www.cinemacity.ro/ro/data-api-service/v1/feed/10107/byName/now-playing?lang=ro_RO",
    "movie_by_code": "https://www.cinemacity.ro/ro/data-api-service/v1/10107/films/byDistributorCode/{movie_code}",
    "cinemas": "https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/cinemas/with-event/until/{todays_date}?attr=&lang=ro_RO",
    "movie_in_cinemas": "https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/cinema-events/in-group/{group_name}/with-film/{movie_code}/at-date/{selected_date}?attr=&lang=ro_RO"
}

DATA_RAW_FOLDER = Path(__file__).resolve().parent / "data" / "raw"


def get_cinemas_folder_path():
    return DATA_RAW_FOLDER


def get_cinemas_json_path():
    DATA_RAW_FOLDER.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    return DATA_RAW_FOLDER / f"cinemas_{date}.json"
