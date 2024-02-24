import pytest
import os
from games.domainmodel.model import *
from games.adapters.datareader.csvdatareader import GameFileCSVReader

from games.adapters.database_repository import *

from tests_db.conftest import *

from datetime import date, datetime
    
    
def test_get_data(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games = repo.get_games()
    assert type(list(games)) == list #assert that it's an object that can be turned into a list
    assert type(list(repo.get_publishers())) == list
    assert type(list(repo.get_genres())) == list
    assert type(list(repo.get_developers())) == list
    

def test_add_game(session_factory): #tests the add_game function to make sure that adding a game to the mem rep adds the game to it's games list.
    repo = SqlAlchemyRepository(session_factory)
    game = Game(1000000, "AGame")
    game.price = 1.2
    game.release_date = "Oct 21, 2008"
    assert game not in repo.get_games()
    repo.add_game(game)
    assert game in repo.get_games()


def test_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = Genre("Test")
    assert genre not in repo.get_genres()
    repo.add_genre(genre)
    assert genre in repo.get_genres()


def test_get_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genres = repo.get_genres()
    genres_list_test = []
    for genre in genres:
        genres_list_test.append(genre.genre_name)
    assert genres_list_test == ['Action',
                                'Adventure',
                                'Casual',
                                'Indie',
                                'Early Access',
                                'Massively Multiplayer',
                                'RPG',
                                'Simulation',
                                'Racing',
                                'Sports',
                                'Strategy',
                                'Free to Play',
                                'Education',
                                'Animation & Modeling',
                                'Audio Production',
                                'Utilities',
                                'Video Production',
                                'Design & Illustration',
                                'Game Development',
                                'Software Training',
                                'Photo Editing',
                                'Web Publishing',
                                'Violent',
                                'Gore']


def test_get_num_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_games = repo.get_number_of_games()
    assert number_of_games == 877


def test_get_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    games = repo.get_games()
    assert type(games) == list
    assert len(games) == 877
    assert games[0].title == 'Xpand Rally'
    
    
def test_get_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_game(3) == None
    assert repo.get_game(7940) == Game(7940, "call of duty")
    assert repo.get_game(40800).title == "Super Meat Boy"


def test_get_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publishers = repo.get_publishers()
    assert type(publishers) == list
    assert len(publishers) == 798
    assert publishers[0].publisher_name == 'Activision'
    
    
def test_set_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publisher1 = Publisher("Jeff")
    publisher2 = Publisher("Kuvi")
    publisher3 = Publisher("Vlex")
    assert Publisher("Vlex") not in repo.get_publishers()
    assert Publisher("Jeff") not in repo.get_publishers()
    assert Publisher("Kuvi") not in repo.get_publishers()
    repo.set_publishers([publisher1, publisher2, publisher3])
    assert Publisher("Kuvi") in repo.get_publishers()
    assert Publisher("Vlex") in repo.get_publishers()
    assert Publisher("Jeff") in repo.get_publishers()
    

def test_get_developers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    developers = repo.get_developers()
    assert type(developers) == list
    assert len(developers) == 842
    assert developers[0].developer_name == 'Infinity Ward'
    
def test_get_games_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    for genre in repo.get_genres():
        games = repo.get_games_by_genre(genre)
        for game in repo.get_games():
            if genre in game.genres:
                assert game in games
            else:
                assert game not in games
                
def test_get_games_by_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    for game_name in repo.get_games():
        game_name = game_name.title
        games = repo.get_games_by_name(game_name)
        for game in repo.get_games():
            if game in games:
                assert game_name.lower() in game.title.lower()
            else:
                assert game_name.lower() not in game.title.lower()
    


def test_get_games_by_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    for publisher in repo.get_publishers():  # does it for every publisher in the list.
        games = repo.get_games_by_publisher(publisher)
        for game in repo.get_games():
            if game in games:
                assert publisher.publisher_name.lower() in game.publisher.publisher_name.lower()
            else:
                assert publisher.publisher_name.lower() not in game.publisher.publisher_name.lower()
