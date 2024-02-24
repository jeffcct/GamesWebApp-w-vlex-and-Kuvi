import pytest
import os
from games.domainmodel.model import *
from games.game import services as game_service
from games.browse import services as browse_service
from games.search import services as search_service
from games.authentication import services as auth_service
from games.favourites import services as favourite_service
from games.wishlist import services as wishlist_service
from tests.conftest import *

"""Game service"""


def test_game_fetching(mem_repo):
    game = game_service.get_game(mem_repo, 7940)
    assert type(game) == Game
    assert game.developer == Developer("Infinity Ward")


"""Browse service"""


def test_human_format_truncate():  # tests all valid possible inputs that need to be truncated
    thousand_value = browse_service.human_format(1000)
    million_value = browse_service.human_format(1000000)
    ten_million_value = browse_service.human_format(10000000)
    hundred_million_value = browse_service.human_format(100000000)
    assert type(thousand_value) == str
    assert hundred_million_value == "100M"
    assert ten_million_value == "10M"
    assert thousand_value == "1K"
    assert million_value == "1M"


def test_human_format_not_rounded():  # check if function can handle not needing to truncate a value
    value = browse_service.human_format(23)
    assert type(value) == str
    assert value == "23"


def test_number_games_repo(mem_repo):  # check if function can return number of games in repo
    assert browse_service.get_number_of_games(mem_repo) == 2


def test_number_games_empty_repos(empty_repo):  # tests if function can handle having an empty repository
    assert browse_service.get_number_of_games(empty_repo) == 0
    with pytest.raises(TypeError) as error:
        browse_service.get_number_of_games()
    assert error.type == TypeError


def test_extract_games(mem_repo):  # tests if function can return list of game objects
    game_dictionary = browse_service.extract_games(mem_repo.get_games())
    assert type(game_dictionary) == list
    assert type(game_dictionary[0]) == dict
    assert len(game_dictionary) == 2
    assert game_dictionary[0]["game_id"] == 7940
    assert game_dictionary[0]["windows"]


def test_extract_empty_games(empty_repo):  # tests if function can return empty list for having no games
    game_dictionary = browse_service.get_games(empty_repo)
    assert type(game_dictionary) == list
    assert len(game_dictionary) == 0


def test_extract_games_by_genre(mem_repo):  # tests if games can be filtered by genre
    game_dictionary = browse_service.get_games_by_genre(mem_repo, "Action")
    assert len(game_dictionary) == 2
    new_dictionary = browse_service.get_games_by_genre(mem_repo, "Adventure")
    assert len(new_dictionary) == 0


def test_get_genres(mem_repo):  # tests if function returns a unique list of genres
    genres = browse_service.get_genres(mem_repo)
    assert len(genres) == 1
    assert type(genres[0]) == Genre
    assert genres[0] == Genre("Action")


def test_get_empty_genres(empty_repo):  # tests if function returns an empty list when searching an empty repo
    genres = browse_service.get_genres(empty_repo)
    assert len(genres) == 0
    assert genres == []


"""Search service"""


def test_search_name_valid(mem_repo):  # tests valid search input
    result = search_service.search_result(mem_repo, "call of duty", "Name")
    assert type(result) == list
    assert type(result[0]) == Game
    assert len(result) == 1


def test_search_name_empty(mem_repo, empty_repo):  # tests empty search input for game name
    result = search_service.search_result(mem_repo, "", "Name")
    empty_result = search_service.search_result(empty_repo, "", "Name")
    assert len(result) == 2
    assert type(result[0]) == Game
    assert len(empty_result) == 0
    with pytest.raises(Exception) as error:
        type(empty_result[0])
    assert error.type == IndexError


def test_search_genre_valid(mem_repo):  # tests for valid search genre
    result = search_service.search_result(mem_repo, "Action", "Genre")
    assert len(result) == 2
    assert type(result[1]) == Game


def test_search_publisher_valid(mem_repo):  # tests for valid publisher name
    result = search_service.search_result(mem_repo, "Activision", "Publisher")
    assert len(result) == 1
    assert result[0].game_id == 7940


"""Authentication service"""


def test_auth_add_user(empty_repo):  # tests for adding user to repo
    auth_service.add_user("Name", "Password", empty_repo)
    user = empty_repo.get_user("name")
    assert type(user) == User
    assert user.username == "name"
    with pytest.raises(auth_service.NameNotUniqueError):  # test for adding same user again
        auth_service.add_user("Name", "Password", empty_repo)
    assert len(user.password) == 102  # checks if password hashed
    assert user.password != "Password"


def test_auth_get_user(mem_repo):
    mem_repo.add_user(User("new_user", "Password"))
    user = auth_service.get_user("new_user", mem_repo)
    assert type(user) == User
    assert user.username == "new_user"
    with pytest.raises(auth_service.UserNotFound):
        auth_service.get_user("doesnt_exist", mem_repo)
    mem_repo.add_user(User("  name  ", "Password1"))
    new_user = auth_service.get_user("  name  ", mem_repo)
    assert type(new_user) == User
    assert new_user.username == "name"


def test_auth_auth_user(mem_repo):  # checks authenticating user
    auth_service.add_user("Name", "Password1", mem_repo)
    auth_service.auth_user("Name", "Password1", mem_repo)  # tests for valid authentication
    with pytest.raises(auth_service.AuthenticationError):
        auth_service.auth_user("Name", "Passwword1", mem_repo)  # tests for invalid password
    with pytest.raises(auth_service.AuthenticationError):
        auth_service.auth_user("Name1", "Password1", mem_repo)  # tests for invalid username

    with pytest.raises(auth_service.AuthenticationError):
        auth_service.auth_user("", "", mem_repo)  # tests for empty authentication


"""Wishlist Services"""


def test_wishlist_add_game_valid(mem_repo_full):  # tests adding game to user's wishlist
    new_user = User("name", "Password")
    new_game = mem_repo_full.get_game(7940)
    wishlist_service.add_to_wishlist(mem_repo_full, new_user, new_game)
    fetched_game = new_user.first_game_in_wishlist()
    assert type(fetched_game) is Game
    assert fetched_game.developer == Developer("Infinity Ward")


def test_wishlist_add_game_invalid(mem_repo_full):  # tests adding an empty game
    new_user = User("name", "Password")
    wishlist_service.add_to_wishlist(mem_repo_full, new_user, None)
    assert new_user.first_game_in_wishlist() is None


def test_wishlist_remove_game_valid(mem_repo_full):  # test removing a game from user's wishlist
    new_user = User("name", "Password")
    new_game = mem_repo_full.get_game(7940)
    wishlist_service.add_to_wishlist(mem_repo_full, new_user, new_game)
    assert new_user.first_game_in_wishlist().developer == Developer("Infinity Ward")
    wishlist_service.remove_from_wishlist(mem_repo_full, new_user, new_game)
    assert new_user.first_game_in_wishlist() is None


def test_wishlist_remove_game_invalid(mem_repo_full):  # tests removing an empty and invalid game
    new_user = User("name", "Password")
    new_game = mem_repo_full.get_game(7940)
    wishlist_service.add_to_wishlist(mem_repo_full, new_user, new_game)
    assert new_user.first_game_in_wishlist().developer == Developer("Infinity Ward")

    wishlist_service.remove_from_wishlist(mem_repo_full, new_user, None)
    assert new_user.first_game_in_wishlist().developer == Developer("Infinity Ward")

    wishlist_service.remove_from_wishlist(mem_repo_full, new_user, Game(79401, "Not COD"))
    assert new_user.first_game_in_wishlist() is not None


def test_wishlist_get_valid_game(mem_repo):
    new_user = User("name", "Password")
    new_game = mem_repo.get_game(7940)
    wishlist_service.add_to_wishlist(mem_repo, new_user, new_game)

    fetched_game = wishlist_service.get_game(mem_repo, 7940)
    assert type(fetched_game) is Game
    assert fetched_game.developer == Developer("Infinity Ward")


def test_wishlist_get_invalid_game(mem_repo):
    new_user = User("name", "Password")
    new_game = mem_repo.get_game(7940)
    wishlist_service.add_to_wishlist(mem_repo, new_user, new_game)

    fetched_game = wishlist_service.get_game(mem_repo, 21)
    assert fetched_game is None


def test_wishlist_fetch_wishlist(mem_repo):
    new_user = User("name", "Password")
    new_game = mem_repo.get_game(7940)
    wishlist_service.add_to_wishlist(mem_repo, new_user, new_game)

    fetched_wishlist = wishlist_service.get_wishlist(mem_repo, new_user)
    assert type(fetched_wishlist) is list

    fetched_wishlist = wishlist_service.get_wishlist(mem_repo, User("Not Valid", "Password1"))
    assert fetched_wishlist == []


"""Favourites Service"""


def test_favourite_add_game_valid(mem_repo_full):  # tests adding game to user's favourite
    new_user = User("name", "Password")
    new_game = mem_repo_full.get_game(7940)
    favourite_service.add_favourite(new_user, new_game, mem_repo_full)
    fetched_game = new_user.favourite_games.list_of_games[0]
    assert type(fetched_game) is Game
    assert fetched_game.developer == Developer("Infinity Ward")


def test_favourite_add_game_invalid(mem_repo_full):  # tests adding an empty game
    new_user = User("name", "Password")
    favourite_service.add_favourite(new_user, None, mem_repo_full)
    assert new_user.favourite_games.list_of_games == []


def test_favourite_remove_game_valid(mem_repo_full):  # test removing a game from user's favourite
    new_user = User("name", "Password")
    new_game = mem_repo_full.get_game(7940)
    favourite_service.add_favourite(new_user, new_game, mem_repo_full)
    assert new_user.favourite_games.list_of_games[0].developer == Developer("Infinity Ward")
    favourite_service.remove_favourite_game(new_user, new_game, mem_repo_full)
    assert new_user.favourite_games.list_of_games == []


def test_favourite_remove_game_invalid(mem_repo_full):  # tests removing an empty and invalid game
    new_user = User("name", "Password")
    new_game = mem_repo_full.get_game(7940)
    favourite_service.add_favourite(new_user, new_game, mem_repo_full)
    assert new_user.favourite_games.list_of_games[0].developer == Developer("Infinity Ward")

    favourite_service.remove_favourite_game(new_user, None, mem_repo_full)
    assert new_user.favourite_games.list_of_games[0].developer == Developer("Infinity Ward")

    favourite_service.remove_favourite_game(new_user, Game(79401, "Not COD"), mem_repo_full)
    assert new_user.favourite_games.list_of_games[0].developer == Developer("Infinity Ward")


def test_favourite_get_valid_game(mem_repo):
    new_user = User("name", "Password")
    new_game = mem_repo.get_game(7940)
    favourite_service.add_favourite(new_user, new_game, mem_repo)

    fetched_game = favourite_service.get_game(mem_repo, 7940)
    assert type(fetched_game) is Game
    assert fetched_game.developer == Developer("Infinity Ward")


def test_favourite_get_invalid_game(mem_repo):
    new_user = User("name", "Password")
    new_game = mem_repo.get_game(7940)
    favourite_service.add_favourite(new_user, new_game, mem_repo)

    fetched_game = favourite_service.get_game(mem_repo, 21)
    assert fetched_game is None


def test_favourite_fetch_favourite(mem_repo):
    new_user = User("name", "Password")
    new_game = mem_repo.get_game(7940)
    favourite_service.add_favourite(new_user, new_game, mem_repo)

    fetched_favourite = favourite_service.get_favourites(new_user, mem_repo)
    assert type(fetched_favourite) is list

    fetched_favourite = favourite_service.get_favourites(User("Not Valid", "Password1"), mem_repo)
    assert fetched_favourite == []
