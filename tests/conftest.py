import pytest
from games import create_app
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import Publisher, Developer, Genre, Game, Review, User, Wishlist
import os
from pathlib import Path
from games.domainmodel.model import User

new_path = Path(__file__).parent
TEST_DATA_PATH = new_path / "data" / "games.csv"
TEST_FULL_DATA_PATH = new_path / "data" / "games_full.csv"


@pytest.fixture
def mem_rep():  # creates a blank memory repository
    return MemoryRepository()


@pytest.fixture
def game():  # creates a list of a single game [list for comparisons]
    games = list()
    games.append(Game(1, "gfhf"))
    return games


@pytest.fixture
def genre():  # creates a list of a single genre [list for comparisons]
    genres = list()
    genres.append(Genre("dfgdf"))
    return genres


@pytest.fixture
def publisher():  # creates a list of a single publisher [list for comparisons]
    publishers = set()
    publishers.add(Publisher("dfggh"))
    return publishers


@pytest.fixture  # creates a list of a single developer [list for comparisons]
def developer():
    developers = set()
    developers.add(Developer("dfjghdf"))
    return developers


@pytest.fixture
def mem_rep2(game, genre, publisher, developer):  # creates a memory repository with one thing in each position
    mem_rep = MemoryRepository()
    mem_rep.add_game(game[0])
    mem_rep.add_genre(genre[0])
    mem_rep.set_publishers(publisher)
    mem_rep.set_developers(developer)
    return mem_rep


@pytest.fixture
def mem_rep3():  # creates a memory repository populated with our data
    mem_rep = MemoryRepository()
    mem_rep.populate()
    return mem_rep


@pytest.fixture
def mem_repo():
    repo = MemoryRepository()
    repo.populate(TEST_DATA_PATH)
    return repo


@pytest.fixture
def user(game):
    user = User("new user", "A totally legitimate password1")
    user.add_favourite_game(game[0])
    user.add_to_wishlist(Game(2, "Another Game"))
    user.add_review(Review(user, game[0], 5, "comment"))
    another_game = Game(3, "")
    user.add_to_wishlist(another_game)
    user.add_favourite_game(another_game)
    return user


@pytest.fixture
def mem_repo_full(user):
    repo1 = MemoryRepository()
    repo1.populate(TEST_FULL_DATA_PATH)
    repo1.add_user(user)
    return repo1


@pytest.fixture
def empty_repo():
    empty_repo = MemoryRepository()
    return empty_repo


"""
@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
"""


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False,
        'SESSION_COOKIE_SECURE': False,  # Disable secure cookies for testing
        'SESSION_COOKIE_HTTPONLY': True,  # Enable httpOnly cookies
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='vlex', password='Qwer1234'):
        return self.__client.post(
            '/login',
            data={'user_name': user_name, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self.__client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


@pytest.fixture()
def new_app():
    app = create_app("something")
    app.config.update({
        "TESTING": True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False,
        'SESSION_COOKIE_SECURE': False,  # Disable secure cookies for testing
        'SESSION_COOKIE_HTTPONLY': True,  # Enable httpOnly cookies
    })
    yield app


@pytest.fixture()
def new_client(new_app):
    return new_app.test_client()


@pytest.fixture()
def new_runner(new_app):
    return new_app.test_cli_runner()
