import pytest
import os
from games.domainmodel.model import Publisher, Developer, Genre, Game, Review, User, Wishlist
from games.profile import services
from tests.conftest import *

# test the services

@pytest.fixture
def list_big():
    return ["11", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"]
    
@pytest.fixture
def list_small():
    return ["1", "2"]

def test_limit_by_type_big(list_big):
    games = services.limit_by_type('game', list_big)
    assert games == ["0", "1", "2", "3", "4"]
    comments = services.limit_by_type("comment", list_big)
    assert comments == ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    
    
def test_by_type_small(list_small):
    games = services.limit_by_type('game', list_small)
    assert games == ["2", "1"]
    comments = services.limit_by_type("comment", list_small)
    assert comments == games
    
def test_get_user(mem_repo_full):
    user = services.get_user(mem_repo_full, "new user")
    user_expected = User("new user", "A totally legitimate password1")
    assert user == user_expected
    user = services.get_user(mem_repo_full, "unadded user")
    assert user == None    
    
def test_get_favourites(mem_repo_full):
    user = services.get_user(mem_repo_full, "new user")
    favourites = services.get_favourites(mem_repo_full, user)
    assert favourites == [Game(3, ""), Game(1, "")] #we don't need the titles as equality of games is tested purely id-wise.
    
    user.add_favourite_game(Game(4, "game"))
    user.add_favourite_game(Game(5, "game"))
    user.add_favourite_game(Game(6, "game"))
    favourites = services.get_favourites(mem_repo_full, user)
    assert favourites == [Game(6, ""), Game(5, ""), Game(4, ""), Game(3, ""), Game(1, "")]
    
    user.add_favourite_game(Game(7, "")) #6'th game, removes means we don't return the oldest game any more
    favourites = services.get_favourites(mem_repo_full, user)
    assert favourites == [Game(7, ""), Game(6, ""), Game(5, ""), Game(4, ""), Game(3, "")]
    
def test_get_wishlist(mem_repo_full):
    user = services.get_user(mem_repo_full, "new user")
    wishlist = services.get_wishlist(mem_repo_full, user)
    assert wishlist == [Game(3, ""), Game(2, "")]
    user.add_to_wishlist(Game(4, ""))
    user.add_to_wishlist(Game(5, ""))
    user.add_to_wishlist(Game(6, ""))
    wishlist = services.get_wishlist(mem_repo_full, user)
    assert wishlist == [Game(6, ""), Game(5, ""), Game(4, ""), Game(3, ""), Game(2, "")]
    user.add_to_wishlist(Game(7, ""))
    wishlist = services.get_wishlist(mem_repo_full, user)
    assert wishlist == [Game(7, ""), Game(6, ""), Game(5, ""), Game(4, ""), Game(3, "")]
    
    
def test_get_comments(mem_repo_full):
    user = services.get_user(mem_repo_full, "new user")
    comments = services.get_comments(mem_repo_full, user)
    assert comments == [Review(user, Game(1, ""), 5, "comment")]
    user.add_review(Review(user, Game(2, ""), 5, "comment"))
    user.add_review(Review(user, Game(3, ""), 5, "comment"))
    user.add_review(Review(user, Game(4, ""), 5, "comment"))
    user.add_review(Review(user, Game(5, ""), 5, "comment"))
    user.add_review(Review(user, Game(6, ""), 5, "comment"))
    user.add_review(Review(user, Game(7, ""), 5, "comment"))
    user.add_review(Review(user, Game(8, ""), 5, "comment"))
    user.add_review(Review(user, Game(9, ""), 5, "comment"))
    user.add_review(Review(user, Game(10, ""), 5, "comment"))
    comments = services.get_comments(mem_repo_full, user)
    assert len(comments) == 10
    assert comments[0].game == Game(10, "")
    games = [comment.game for comment in comments]
    assert Game(1, "") in games
    
    user.add_review(Review(user, Game(11, ""), 5, "comment"))
    comments = services.get_comments(mem_repo_full, user)
    assert len(comments) == 10
    assert comments[0].game == Game(11, "")
    games = [comment.game for comment in comments]
    assert Game(1, "") not in games
    
    
def test_update_profile(mem_repo_full):
    user = services.get_user(mem_repo_full, "new user")
    profile = user.profile
    start_description = profile.description
    start_fav = profile.show_favourites
    start_wish = profile.show_wishlist
    start_comm = profile.show_comments
    services.update_profile(mem_repo_full, "new description", True, False, False, "new user")
    assert start_description != profile.description
    assert profile.description == "new description"
    assert start_fav == profile.show_favourites
    assert start_wish != profile.show_wishlist
    assert start_comm != profile.show_comments
    services.update_profile(mem_repo_full, "new description", False, True, True, "new user")
    assert profile.description == "new description"
    assert start_fav != profile.show_favourites
    assert start_wish == profile.show_wishlist
    assert start_comm == profile.show_comments
    other_user = User("other_user", "TotallyLegitPassw0rd")
    mem_repo_full.add_user(other_user)
    assert other_user.profile.description != profile.description
    assert other_user.profile.show_favourites != profile.show_favourites
    services.update_profile(mem_repo_full, "new description", False, True, True, "new user")
    assert other_user.profile.description != profile.description
    assert other_user.profile.show_favourites != profile.show_favourites
    start_description = profile.description
    start_fav = profile.show_favourites
    start_wish = profile.show_wishlist
    start_comm = profile.show_comments
    services.update_profile(mem_repo_full, "new descption", True, False, True, "other_user")
    assert start_description == profile.description
    assert start_fav == profile.show_favourites
    assert start_wish == profile.show_wishlist
    assert start_comm == profile.show_comments
    assert other_user.profile.description == "new descption"
    
    
def test_get_current_settings(mem_repo_full):
    user = services.get_user(mem_repo_full, "new user")
    test_comm, test_fav, test_wish, test_desc = services.get_current_settings(mem_repo_full, "new user")
    assert test_comm == user.profile.show_comments
    assert test_fav == user.profile.show_favourites
    assert test_wish == user.profile.show_wishlist
    assert test_desc == user.profile.description
    services.update_profile(mem_repo_full, "new description", False, True, True, "new user")
    test_comm, test_fav, test_wish, test_desc = services.get_current_settings(mem_repo_full, "new user")
    assert test_comm == user.profile.show_comments and test_fav == user.profile.show_favourites and test_wish == user.profile.show_wishlist and test_desc == user.profile.description
    services.update_profile(mem_repo_full, "new description", False, True, True, "new user")
    test_comm, test_fav, test_wish, test_desc = services.get_current_settings(mem_repo_full, "new user")
    assert test_comm == user.profile.show_comments and test_fav == user.profile.show_favourites and test_wish == user.profile.show_wishlist and test_desc == user.profile.description