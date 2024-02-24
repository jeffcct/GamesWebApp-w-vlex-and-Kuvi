import os
from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import *
from games.adapters.datareader.csvdatareader import GameFileCSVReader

from sqlalchemy import delete, select
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from .orm import game_genres_table, Genre, Game, User, wishlist_game_table, user_table


from .orm import game_genres_table




class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self.__session_cm = SessionContextManager(session_factory)

    def add_game(self, game):
        with self.__session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def close_session(self):
        self.__session_cm.close_current_session()


    def reset_session(self):
        self.__session_cm.reset_session()
        
    
     # to be implemented       
    def get_games(self):
        try:
            return self.__session_cm.session.query(Game).all()
        except NoResultFound:
            return []

    def get_game(self, game_id):
        game = None
        try:
            game = self.__session_cm.session.query(Game).\
                filter(Game._Game__game_id == game_id).one()
            return game
        except NoResultFound:
            print(f'Game {game_id} was not found')
            return None
    
    
    #this is not working
    def get_games_by_genre(self, genre):
        try:
            games = self.__session_cm.session.query(Game).\
                join(game_genres_table).\
                filter(game_genres_table.c.genre_name.like(f'%{genre.genre_name}%')).\
                order_by(Game._Game__game_id).all()
            return games
        except NoResultFound:
            return []
    #end of this is not working
    
    def get_games_by_publisher(self, publisher):
        try:
            games = self.__session_cm.session.query(Game).\
                join(Publisher).\
                filter(Publisher._Publisher__publisher_name.like(f'%{publisher.publisher_name}%')).\
                order_by(Game._Game__game_id).all()
            return games
        except NoResultFound:
            return []
    
    def get_games_by_name(self, game_name):
        try:
            games = self.__session_cm.session.query(Game).\
                filter(Game._Game__game_title.like(f"%{game_name}%")).\
                order_by(Game._Game__game_id).all()
            return games
        except NoResultFound:
            return []
    
    def get_number_of_games(self):
        return self.__session_cm.session.query(Game).\
        count()
    
    def get_genres(self):
        return self.__session_cm.session.query(Genre).all()
    
    def get_developers(self):
        return self.__session_cm.session.query(Developer).all()
    
    def get_publishers(self):
        return self.__session_cm.session.query(Publisher).all()

    
    def set_publishers(self, publishers):
        for publisher in publishers:
            self.add_publisher(publisher)
    
    def get_user(self, username):
        try:
            user = self.__session_cm.session.query(User).\
                filter(User._User__username == username).one()
            return user
        except NoResultFound:
            return None

    #to be implemented

    def add_user(self, user):
        with self.__session_cm as scm:
            scm.session.add(user)
            scm.commit()


    def add_genre(self, genre):
        with self.__session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_developer(self, developer):
        with self.__session_cm as scm:
            scm.session.merge(developer)
            scm.commit()

    def add_publisher(self, publisher):
        with self.__session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_screenshot(self, screenshot):
        with self.__session_cm as scm:
            scm.session.merge(screenshot)
            scm.commit()

    def add_trailer(self, trailer):
        with self.__session_cm as scm:
            scm.session.merge(trailer)
            scm.commit()

    def add_category(self, category):
        with self.__session_cm as scm:
            scm.session.merge(category)
            scm.commit()
            
    def add_comment(self, comment, rating, user, game):
        try:
            comment = Review(user, game, rating, comment)

            with self.__session_cm as scm:
                scm.session.merge(comment)
                scm.session.merge(game)
                scm.commit()
        except:
            self.__session_cm.session.rollback()
            
            
    def add_favourite_game(self, user, game):
        try:
            user = self.__session_cm.session.query(User).filter(User._User__username == user.username).one()
            game = self.__session_cm.session.query(Game).filter(Game._Game__game_id == game.game_id).one()
            user.add_favourite_game(game)
            self.__session_cm.session.commit()
        except NoResultFound:
            self.__session_cm.session.rollback()
            raise
    
    def add_to_wishlist(self, user, game):
        try:
            user = self.__session_cm.session.query(User).filter(User._User__username == user.username).one()
            game = self.__session_cm.session.query(Game).filter(Game._Game__game_id == game.game_id).one()

            user.add_to_wishlist(game)

            self.__session_cm.session.commit()

        except NoResultFound:
            self.__session_cm.session.rollback()
            raise
        
    def remove_favourite_game(self, user1, game):
        try:
            user = self.__session_cm.session.query(User).filter(User._User__username == user1.username).one()
            game = self.__session_cm.session.query(Game).filter(Game._Game__game_id == game.game_id).one()
            user.remove_favourite_game(game)
            self.__session_cm.session.commit()

        except NoResultFound:
            self.__session_cm.session.rollback()
            raise
        
    def remove_from_wishlist(self, user1: User, game):
        try:
            user = self.__session_cm.session.query(User).filter(User._User__username == user1.username).one()
            game = self.__session_cm.session.query(Game).filter(Game._Game__game_id == game.game_id).one()
            user.remove_from_wishlist(game)
            self.__session_cm.session.commit()

        except NoResultFound:
            self.__session_cm.session.rollback()
            raise
        
    
    def get_wishlist(self, user):
        print("tried getting withlist")
        try:
            user = self.__session_cm.session.query(User).filter(User._User__username == user.username).one()
            wishlist = user.wishlist
            return list(wishlist)
        except NoResultFound:
            return []
    
    def get_favourites(self, user):
        print("tried getting favourites")
        try:
            user = self.__session_cm.session.query(User).filter(User._User__username == user.username).one()
            favourites = user.favourite_games
            return list(favourites)
        except NoResultFound:
            return []
    
    def get_reviews(self, user):
        print("tried getting reviews")
        try:
            user = self.__session_cm.session.query(Review).\
                filter(Review._Review__user == user).all()
            return user
        except NoResultFound:
            return None
        
    def update_profile(self, description, favourites, wishlist, comments, user):
        profile = user.profile
        profile.description = description
        profile.show_favourites = favourites
        profile.show_wishlist = wishlist
        profile.show_comments = comments
        with self.__session_cm as scm:
            scm.session.merge(profile)
            scm.commit()

            

    def populate(self, data_path: Path):
        game_file_name = str(Path(data_path) / "games.csv")
        reader = GameFileCSVReader(game_file_name)
        reader.read_csv_file()

        games = reader.dataset_of_games
        genres = reader.dataset_of_genres
        publishers = reader.dataset_of_publishers
        developers = reader.dataset_of_developers
        categories = reader.dataset_of_categories
        trailers = reader.dataset_of_trailers
        screenshots = reader.dataset_of_screenshots

        for game in games:
            self.add_game(game)

        for genre in genres:
            self.add_genre(genre)

        for publisher in publishers:
            self.add_publisher(publisher)

        for developer in developers:
            self.add_developer(developer)

        for category in categories:
            self.add_category(category)

        for trailer in trailers:
            self.add_trailer(trailer)

        for screenshot in screenshots:
            self.add_screenshot(screenshot)

