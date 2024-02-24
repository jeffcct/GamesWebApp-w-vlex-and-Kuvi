from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher


def search_result(repo: AbstractRepository, query: str, category: str):
    if category == "Genre":
        try:
            genre_query = Genre(query.lower())
            return repo.get_games_by_genre(genre_query)
        except TypeError:
            return []
        except ValueError:
            return []
        except IndexError:
            return []

    elif category == "Publisher":
        try:
            publisher_query = Publisher(query.lower())
            return repo.get_games_by_publisher(publisher_query)
        except TypeError:
            return []
        except ValueError:
            return []


    elif category == "Name":
        try:
            return repo.get_games_by_name(query.lower())
        except ValueError:
            return []
        except TypeError:
            return []

    else:
        return []

# try parse query then call specific function from mem repo, parse fail then raise error
# also handle if list returned is empty


# for genre and publisher, try parse as object, if object not in dataset, raise error
