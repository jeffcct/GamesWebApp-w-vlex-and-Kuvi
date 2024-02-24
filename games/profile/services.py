from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User
from games.authentication.services import UserNotFound

# used to define the maximum amount to be displayed on the homepage
types = {'game': 5, 'comment': 10}


def limit_by_type(type, items):
    if len(items) > types[type]:
        return items[len(items) - 1: len(items) - types[type] - 1: -1]
    return items[::-1]


def get_user(repo: AbstractRepository, user: str):
    new_user = repo.get_user(user)
    return new_user


def get_favourites(repo: AbstractRepository, user: User):
    if user is None:
        raise UserNotFound
    favourites = repo.get_favourites(user)
    return limit_by_type('game', favourites)


def get_wishlist(repo: AbstractRepository, user: User):
    if user is None:
        raise UserNotFound
    wishlist = repo.get_wishlist(user)
    return limit_by_type('game', wishlist)


def get_comments(repo: AbstractRepository, user: User):
    reviews = repo.get_reviews(user)
    return limit_by_type('comment', reviews)


def update_profile(repo, description, favourites, wishlist, comments, user):
    user = repo.get_user(user)
    repo.update_profile(description, favourites, wishlist, comments, user)


def get_current_settings(repo: AbstractRepository, user_name: str):
    user = get_user(repo, user_name)
    if user is None:
        raise UserNotFound
    return user.profile.show_comments, user.profile.show_favourites, user.profile.show_wishlist, user.profile.description
