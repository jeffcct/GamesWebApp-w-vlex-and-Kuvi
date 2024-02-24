import os
from bisect import insort_left
from typing import List, Set

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher, Developer, User, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__games = list()
        self.__publishers = set()
        self.__genres = list()
        self.__developers = set()
        self.__users = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            if game in self.__games:
                return False
            #  uses insort_left from the bisect module to keep game list sorted by id when inserting game
            insort_left(self.__games, game)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            insort_left(self.__genres, genre)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def get_game(self, game_id: int):
        for game in self.__games:
            if game.game_id == game_id:
                return game
        return None

    def get_publishers(self) -> Set[Publisher]:
        return self.__publishers

    def set_publishers(self, publisher_set):
        self.__publishers = publisher_set

    def get_developers(self) -> Set[Developer]:
        return self.__developers

    def set_developers(self, developer_set):
        self.__developers = developer_set

    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        out_games = []
        for game in self.__games:
            for game_genre in game.genres:
                if genre.genre_name.lower() in game_genre.genre_name.lower():
                    out_games.append(game)
                    break
        return out_games

        # return [game for game in self.__games if genre in game.genres]

    def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:
        return [game for game in self.__games if
                publisher.publisher_name.lower() in game.publisher.publisher_name.lower()]

    def get_games_by_name(self, game_name: str) -> List[Game]:
        return [game for game in self.__games if game_name.lower() in game.title.lower()]

    def add_user(self, user: User):
        self.__users.append(user)
        
    def add_comment(self, comment, rating, user, game):
        comment = Review(user, game, rating, comment)
    
    def get_user(self, username: str):
        for user in self.__users:
            if user.username == username:
                return user
        return None

    
    def add_favourite_game(self, user, game):
        user.add_favourite_game(game)
        
    def remove_favourite_game(self, user, game):
        user.remove_favourite_game(game)
        
    def get_favourites(self, user):
        return user.favourite_games.list_of_games
    
    
    def add_to_wishlist(self, user, game):
        user.add_to_wishlist(game)
        
    def remove_from_wishlist(self, user, game):
        user.remove_from_wishlist(game)
    
    def get_wishlist(self, user):
        return user.wishlist.list_of_games
    
    
    def get_reviews(self, user):
        return user.reviews
    
    def update_profile(self, description, favourites, wishlist, comments, user):
        profile = user.profile
        profile.description = description
        profile.show_favourites = favourites
        profile.show_wishlist = wishlist
        profile.show_comments = comments
        

    def populate(self, path="data/games.csv"):
        dir_name = os.path.dirname(os.path.abspath(__file__))
        games_file_name = os.path.join(dir_name, path)
        reader = GameFileCSVReader(games_file_name)

        reader.read_csv_file()

        games = reader.dataset_of_games
        genres = reader.dataset_of_genres
        self.set_publishers(reader.dataset_of_publishers)
        self.set_developers(reader.dataset_of_developers)

        #  add games to the repo
        for game in games:
            self.add_game(game)

        for genre1 in genres:
            self.add_genre(genre1)
