from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Review, User


def get_game(repo: AbstractRepository, game_id: int):
    return repo.get_game(game_id)

def add_comment(repo: AbstractRepository, comment, rating, user, game):
        user = repo.get_user(user)
        repo.add_comment(comment, rating, user, game)
        
    


