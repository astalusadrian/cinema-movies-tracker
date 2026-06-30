from api import MoviesAPI
from endpoints import get_cinemas_folder_path

if __name__ == "__main__":
    api = MoviesAPI()
    api.run()
    # -> Currently getting cinemas data from the API and creating a snapshot of it.