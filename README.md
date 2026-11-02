# Cinema Movies Tracker

A lightweight Python project for exploring movies and cinema data from Cinemacity Romania using the public API endpoints exposed by the site.

This repository is a useful starting point for:
- pulling "now playing" and "coming soon" movie data
- inspecting movie metadata such as codes, titles, attributes, and dates
- saving raw API responses for offline analysis
- experimenting with cinema and screening data from the Cinemacity endpoints

It is intentionally small and easy to extend, making it a good template for API-backed movie tracking projects.

## Features

- Fetches movie data from Cinemacity's public feeds
- Consolidates movies by unique code to avoid duplicate entries
- Extracts relevant fields like title, code, URL, start date, and type
- Stores raw JSON API responses for future inspection
- Includes a simple interactive CLI for quick local testing

## Project structure

```text
cinema-movies-tracker/
├── README.md
├── main.py                  # interactive command-line entry point
├── api.py                   # wrapper for API requests and movie parsing
├── config.py                # endpoint configuration and helper paths
├── data/
│   └── raw/                 # local store for generated daily snapshots
└── .gitignore               # excludes generated data and local artifacts
```

## What the project currently does

The current implementation focuses on movie discovery and data collection:

- `coming_soon` feed: upcoming films
- `now_playing` feed: currently screened films
- `movie_in_cinemas`/`cinemas` endpoints: cinema-related data and event lookups

## Requirements

- Python 3.9+
- `requests`

Install dependencies:

```bash
pip install requests
```

## Getting started

1. Clone the repository:

```bash
git clone https://github.com/astalusadrian/cinema-movies-tracker.git
cd cinema-movies-tracker
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

3. Install requirements:

```bash
pip install requests
```

4. Run the interactive CLI:

```bash
python main.py
```

You will see a menu with actions such as:
- List movies
- List cinemas

## Example usage

### Inspect a movie list

```python
from api import MoviesAPI

api = MoviesAPI()
movies = api.get_movies_list()
print(movies)
```

The returned data is grouped by movie code and includes sections such as `coming_soon` and `now_playing`.

## Data model

The project largely works with the structure returned by Cinemacity's `body.posters` response. Each movie entry can include fields like:

- `code`
- `featureTitle`
- `url`
- `dateStarted`
- `attributes`
- `filmShowingType`

The code is used as the unique identity for merging entries across categories.

## Important notes

- This project depends on external public endpoints, so the API may change without notice.
- The repository includes sample JSON files but is not a full production-ready app.
- Cinema listing logic is still scaffolded in `api.py`, so some features may be incomplete or require additional development.
- Networking access is required to fetch fresh data from Cinemacity.

## Future ideas

Some good extensions for this project include:
- storing movie data in SQLite or CSV
- comparing daily movie feeds to detect new releases
- mapping movies to local cinema screenings by city/date
- building a small dashboard or web interface
- adding filtering by genre, language, or cinema group
