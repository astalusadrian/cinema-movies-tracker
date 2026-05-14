from api import MoviesAPI
import sys


if __name__ == "__main__":
    api = MoviesAPI()

    print(api.get_cinemas_cache())
    print(api.get_movies_in_cinema('Târgu Mureș PlazaM'))