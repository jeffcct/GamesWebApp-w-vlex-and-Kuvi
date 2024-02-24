from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User
from werkzeug.security import generate_password_hash, check_password_hash


class AuthenticationError(Exception):
    pass


class NameNotUniqueError(Exception):
    pass


class UserNotFound(Exception):
    pass


def add_user(user: str, password: str, repo: AbstractRepository):
    user = user.lower().strip()
    new_user = repo.get_user(user)
    if new_user is not None:
        raise NameNotUniqueError

    password_hashed = generate_password_hash(password)
    new_user1 = User(user, password_hashed)
    repo.add_user(new_user1)


def get_user(user: str, repo: AbstractRepository):
    user = user.lower().strip()
    new_user = repo.get_user(user)
    if new_user is None:
        raise UserNotFound
    return new_user


def auth_user(user: str, password: str, repo: AbstractRepository):
    user = user.lower().strip()
    authenticated = False

    check_user = repo.get_user(user)
    if check_user is not None:
        authenticated = check_password_hash(check_user.password, password)

    if not authenticated:
        raise AuthenticationError
