import abc
from typing import List, Set
from games.domainmodel.model import Game, Genre, Publisher, Developer, User

repo_instance = None  # global instance of repo


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
    """Storing data"""

    @abc.abstractmethod
    def add_game(self, game: Game):  # adds game to repo
        raise NotImplementedError

    """Fetching data"""

    @abc.abstractmethod
    def get_games(self) -> List[Game]:  # returns list of all games
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id: int):  # retrieves game from list
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre: Genre) -> List[Game]:  # return list of games with specific genre
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:  # return list of games by publisher
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_name(self, game_name: str):  # return game by name
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self) -> int:  # returns number of games
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:  # returns list of unique genres
        raise NotImplementedError

    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_developers(self) -> List[Developer]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self) -> Set[Publisher]:  # returns list of publishers
        raise NotImplementedError

    @abc.abstractmethod
    def set_publishers(self, publisher_set: set):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError
    """
    @abc.abstractmethod
    def get_genre_of_game(self, game_id):  # returns list of genres of a specific game
        raise NotImplementedError

    """

    # added 09/10for db repo
    @abc.abstractmethod
    def get_favourites(self, user: User):
        raise NotImplementedError


    # added 09/10for db repo
    @abc.abstractmethod
    def add_favourite_game(self, user: User, game: Game):
        raise NotImplementedError


    # added 09/10for db repo
    @abc.abstractmethod
    def remove_favourite_game(self, user: User, game: Game):
        raise NotImplementedError


    # added 09/10for db repo
    @abc.abstractmethod
    def get_wishlist(self, user: User):
        raise NotImplementedError


    # added 09/10 for db repo
    @abc.abstractmethod
    def add_to_wishlist(self, user: User, game: Game):
        raise NotImplementedError


    #added 09/10 for db repo
    @abc.abstractmethod
    def remove_from_wishlist(self, user: User, game: Game):
        raise NotImplementedError

