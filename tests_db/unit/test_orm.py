import pytest

from sqlalchemy.exc import IntegrityError
from typing import List

from games.domainmodel.model import User, Game, Wishlist, Publisher, Review, Genre

from tests_db.conftest import empty_session


def make_user():
    user = User('name_new', "Password123")
    return user


def make_manual_user(username, password):
    user = User(username, password)
    return user


def make_game():
    game = Game(1234, "New_Game")
    game.price = 60.01
    game.release_date = "Oct 21, 2008"
    return game


def make_genre():
    genre = Genre("ActionRPG")
    return genre


def make_review(game: Game):
    review = Review(make_user(), game, 3, "Good Game")
    return review



def insert_user(empty_session, users: List[User]):
    for user in users:
        empty_session.execute('INSERT INTO users (name, password) VALUES (:user_name, :password)',
                              {'user_name': user.username, 'password': user.password})      # manually add user to table


def insert_games(empty_session, games: List[Game]):
    for game in games:
        empty_session.execute('INSERT INTO games (id, game_title, game_price, release_date, average_rating) VALUES (:id, :title, :price, "0", 0)',
                              {'id': game.game_id, 'title': game.title, 'price': game.price})    # manually add multiple games to table

def insert_review(empty_session, review: Review):
    empty_session.execute('INSERT INTO reviews (game_id, comment, rating) VALUES (:game, :comment, :rating)',
                          {'game': review.game.game_id, 'comment': review.comment, 'rating': review.rating})


def test_get_user(empty_session):
    insert_user(empty_session, [make_user(), make_manual_user("helloworld", "Password123")])
    users = empty_session.query(User).all()
    assert type(users[0]) == User
    assert users[0].username == "name_new"
    assert users[1].username == "helloworld"


def test_save_user(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT name FROM users'))
    assert rows == [("name_new",)]


def test_save_duplicate_user(empty_session):
    user = make_user()
    user1 = make_user()

    empty_session.add(user)
    empty_session.commit()

    with pytest.raises(IntegrityError):
        empty_session.add(user1)
        empty_session.commit()

def test_get_games(empty_session):
    new_game = Game(43254, "Another_game")
    new_game.price = 12.34
    insert_games(empty_session, [make_game(), new_game])

    games = list(empty_session.query(Game))

    assert type(games[0]) == Game
    assert games[1].game_id == 43254

def test_save_game(empty_session):
    empty_session.add(make_game())
    empty_session.commit()

    rows = list(empty_session.execute('SELECT * from games'))
    assert rows[0][0] == 1234

def test_get_review(empty_session):
    insert_review(empty_session, make_review(make_game()))

    rows = list(empty_session.query(Review))
    assert type(rows[0]) == Review
    assert rows[0].rating == 3

def test_save_review(empty_session):
    empty_session.add(make_review(make_game()))
    empty_session.commit()

    rows = list(empty_session.execute('SELECT comment from reviews WHERE reviews.id = 1'))
    assert rows[0][0] == 'Good Game'


def test_save_game_with_review(empty_session):

    game = make_game()
    review = make_review(game)

    game.add_review(review)

    empty_session.add(game)
    empty_session.commit()

    row = list(empty_session.query(Game))
    assert row[0].reviews[0] == review

    entry = list(empty_session.execute('SELECT comment from reviews'))
    assert entry[0][0] == "Good Game"

    users = list(empty_session.execute('SELECT user_id from reviews'))
    assert users[0][0] == 1


def test_save_game_with_genre(empty_session):
    game = make_game()
    genre = make_genre()

    game.add_genre(genre)
    empty_session.add(game)
    empty_session.commit()

    row = list(empty_session.query(Game))
    assert row[0].genres[0] == genre

    query = list(empty_session.execute('SELECT * FROM games_genre_assoc'))
    assert query[0][2] == "ActionRPG"