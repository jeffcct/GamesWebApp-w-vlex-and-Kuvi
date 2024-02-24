from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User, Wishlist, Game
import games.game.services as game_services
from flask import redirect, url_for
from games.authentication.services import UserNotFound

# wishlists = {}    # redundant, but may be useful if Wishlist class is used in the future


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    return user


"""
# redundant, but may be useful if Wishlist class is used in the future
def get_wishlist(user: User):
    # wishlist = Wishlist(user)
    # return wishlist.list_of_games()
    # return wishlist
    
    if user.username in wishlists:
        # If the user already has a wishlist, return the existing one.
        return wishlists[user.username]
    else:
        # If the user doesn't have a wishlist, create a new one and store it.
        wishlist = Wishlist(user)
        wishlists[user.username] = wishlist
        return wishlist
"""


"""
def get_wishlist(user: User):
    if user is None:
        raise UserNotFound
    return user.wishlist
"""
def get_wishlist(repo:AbstractRepository, user: User):
    if user is None:
        raise UserNotFound
    return repo.get_wishlist(user)


def get_game(repo: AbstractRepository, game_id: int):
    return game_services.get_game(repo, game_id)


"""
def add_to_wishlist(user: User, game: Game):
    user.add_to_wishlist(game)
"""
#refactor for db
def add_to_wishlist(repo:AbstractRepository, user: User, game: Game):
    repo.add_to_wishlist(user, game)


"""
def remove_from_wishlist(user: User, game: Game):
    user.remove_from_wishlist(game)
"""
# 09/10 refactor for db
def remove_from_wishlist(repo:AbstractRepository, user: User, game: Game):
    repo.remove_from_wishlist(user, game)
