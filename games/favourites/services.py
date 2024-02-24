from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Game
# import games.authentication.services as authentication_services
import games.game.services as game_services
from games.authentication.services import UserNotFound


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    return user


def get_game(repo: AbstractRepository, game_id: int):
    return game_services.get_game(repo, game_id)

  
def get_favourites(user: User, repo: AbstractRepository):
    if user is None:
        raise UserNotFound
    return repo.get_favourites(user) 


def add_favourite(user: User, game: Game, repo: AbstractRepository):
    repo.add_favourite_game(user, game)

def remove_favourite_game(user: User, game: Game, repo: AbstractRepository):
    repo.remove_favourite_game(user, game)