from api import MoviesAPI

if __name__ == "__main__":
    api = MoviesAPI()

    actions = {
        "1": ("List movies", api.get_movies_list),
        "2": ("List cinemas", api.get_cinemas),
    }

    while True:
        print('\nSelect an action:')
        for choice, (description, _) in actions.items():
            print(f"{choice}. {description}")
        print("0. Exit")

        choice = input("> ").strip()

        if choice == "0":
            print("Exiting...")
            break

        action = actions.get(choice)
        if action:
            _, func = action
            result = func()
            print(result)
        else:
            print("Invalid choice. Please try again.")
