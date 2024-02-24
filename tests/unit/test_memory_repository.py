import pytest
import os
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader

from games.adapters.memory_repository import *

from tests.conftest import *



    

def test_populate(mem_rep):  #tests the populate function, makes sure the original mem_rep is empty, then after populate it has the right number of things in it.
    assert mem_rep.get_games() == list()
    assert mem_rep.get_genres() == list()
    assert mem_rep.get_publishers() == set()
    assert mem_rep.get_developers() == set()
    mem_rep.populate()
    assert len(mem_rep.get_games()) == 877
    assert len(mem_rep.get_genres()) == 24
    assert len(mem_rep.get_publishers()) == 798
    assert len(mem_rep.get_developers()) == 842
    
    

def test_memrep_init(): #tests the init function for the memory repo, makes sure it starts with the correct starting states.
    mem_rep = MemoryRepository()
    assert mem_rep.get_games() == list()
    assert mem_rep.get_publishers() == set()
    assert mem_rep.get_genres() == list()
    assert mem_rep.get_developers() == set()
    

def test_add_game(mem_rep, game): #tests the add_game function to make sure that adding a game to the mem rep adds the game to it's games list.
    assert mem_rep.get_games() == list()
    mem_rep.add_game(game[0])
    assert mem_rep.get_games() == game
    
def test_add_genre(mem_rep, genre): #tests the add_genre function to make sure adding a genre adds the genre to the list of genres.
    assert mem_rep.get_genres() == list()
    mem_rep.add_genre(genre[0])
    assert mem_rep.get_genres() == genre
    
def test_get_games(mem_rep, mem_rep2, game): #mem_rep_2 has games as it's list of games, mem_rep has no games
    assert mem_rep2.get_games() == game
    assert mem_rep.get_games() == list()
    
def test_get_genres(mem_rep, mem_rep2, genre): #mem_rep2 has genres as it's list of games, mem_rep has no games
    assert mem_rep2.get_genres() == genre
    assert mem_rep.get_genres() == list()
    
def test_get_num_games(mem_rep, mem_rep2, mem_rep3): #tests the get_num_games function based on the 3 mem_rep cases.
    assert mem_rep.get_number_of_games() == 0
    assert mem_rep2.get_number_of_games() == 1
    assert mem_rep3.get_number_of_games() == 877
    
def test_get_game(mem_rep2, game, mem_rep3): #mem_rep2 has one game, and it's id = 1, tests to make sure it's in mem_rep2. also tests a random game in mem_rep3.
    assert mem_rep2.get_game(3) == None
    assert mem_rep2.get_game(1) == game[0]
    assert mem_rep3.get_game(40800).title == "Super Meat Boy"
    
def test_get_publishers(mem_rep, mem_rep2, mem_rep3, publisher): #tests the get_publisher function to make sure each of the mem reps have the right data.
    assert mem_rep.get_publishers() == set()
    assert mem_rep2.get_publishers() == publisher
    assert len(mem_rep3.get_publishers()) == 798
    
def test_set_publishers(mem_rep, publisher): #tests the set_publisher() function to make sure it changes the publishers to the given publishers
    assert mem_rep.get_publishers() == set()
    mem_rep.set_publishers(publisher)
    assert mem_rep.get_publishers() == publisher
    
def test_get_developers(mem_rep, developer): #tests the get_developers() function to make sure it returns the correct list of developers
    assert mem_rep.get_developers() == set()
    mem_rep.set_developers(developer)
    assert mem_rep.get_developers() == developer
    
def test_set_developers(mem_rep, publisher): #tests the set_developers() function to make sure it sets the developers correctly.
    assert mem_rep.get_developers() == set()
    mem_rep.set_developers(developer)
    assert mem_rep.get_developers() == developer
    
def test_get_games_by_genre(mem_rep3): #tests the get_games_by_genre function to make sure that it returns all games of a genre, and no games not of the genre.
    for genre in mem_rep3.get_genres(): #does it for every genre
        games = mem_rep3.get_games_by_genre(genre)
        for game in mem_rep3.get_games():
            if genre in game.genres:
                assert game in games
            else:
                assert game not in games
                
def test_get_games_by_publisher(mem_rep3): # tests the get_games_by_publsiher function to make sure that it returns all games by an input publisher and no games by different publsihers
    for publisher in mem_rep3.get_publishers(): #does it for every publisher in the list.
        games = mem_rep3.get_games_by_publisher(publisher)
        for game in mem_rep3.get_games():
            if game in games:
                assert publisher.publisher_name.lower() in game.publisher.publisher_name.lower()
            else:
                assert publisher.publisher_name.lower() not in game.publisher.publisher_name.lower()
                
def test_game_by_name(mem_rep3): # tests the get_games_by_name function to make sure it returns all the games with an input text inside of it (i.e "me" would still return a game called "game game")
    for game_name in mem_rep3.get_games(): #does it for every name of a game
        game_name = game_name.title
        games = mem_rep3.get_games_by_name(game_name)
        for game in mem_rep3.get_games():
            if game in games:
                assert game_name.lower() in game.title.lower()
            else:
                assert game_name.lower() not in game.title.lower()

