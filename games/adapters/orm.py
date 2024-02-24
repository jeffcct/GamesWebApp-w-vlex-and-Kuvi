from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey, UniqueConstraint, Boolean
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Publisher, Genre, Review, User, Developer, Wishlist, Profile, Trailer, Screenshot, Favourites

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

developer_table = Table(
    'developers', metadata,
    Column('name', String(255), primary_key=True),
)

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True),
)

games_table = Table(
    'games', metadata,
    Column('id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(1023), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name')),
    Column('developer_name', String(255), ForeignKey('developers.name')),
    Column('achievements', Integer, nullable=True),
    Column('recommendations', Integer, nullable=True),
    Column('notes', String(1000), nullable=True),
    Column('windows', Boolean),
    Column('apple', Boolean),
    Column('linux', Boolean),
    Column('average_rating', Float, default=0),
)

genres_table = Table(
    'genres', metadata,
    Column('name', String(64), primary_key=True, nullable=False)
)

"""category_table = Table(
    'categories', metadata,
    Column('name', String(255), primary_key=True),
)"""

game_genres_table = Table(
    'games_genre_assoc', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('genre_name', Integer, ForeignKey('genres.name')),
    UniqueConstraint('game_id', 'genre_name'),
)

"""game_category_table = Table(
    'game_category_assoc', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', Integer, ForeignKey("games.id")),
    #Column('category_name', String(255), ForeignKey('categories.name')),
    UniqueConstraint('game_id', 'category_name'),
)"""

user_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True),
    Column('password', String(255)),
    Column('profile_id', Integer, ForeignKey('profile.id')),
    Column('favourites_id', Integer, ForeignKey('favourites.id')),
    Column('wishlist_id', Integer, ForeignKey('wishlist.id')),
    
)

review_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('comment', String(1023)),
    Column('rating', Integer),
    UniqueConstraint('user_id', 'game_id'),
)

wishlist_table = Table(
    'wishlist', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
)

wishlist_game_table = Table(
    'wishlist_game_assoc', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('wishlist_id', Integer, ForeignKey('wishlist.id')),
    Column('game_id', Integer, ForeignKey('games.id')),
    UniqueConstraint('wishlist_id', 'game_id'),
)

favourites_table = Table(
    'favourites', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
)

favourites_game_table = Table(
    'favourites_game_assoc', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('favourites_id', Integer, ForeignKey('favourites.id')),
    Column('game_id', Integer, ForeignKey('games.id')),
    UniqueConstraint('favourites_id', 'game_id'),
)

profile_table = Table(
    'profile', metadata,
    Column('id', Integer, primary_key=True),
    Column('description', String(2047)),
    Column('show_wishlist', Boolean),
    Column('show_favourites', Boolean),
    Column('show_comments', Boolean),
)


trailer_table = Table(
    'trailer', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('link', String(255)),
    Column('game_id', Integer, ForeignKey("games.id")),
)

screenshot_table = Table(
    'screenshot', metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('link', String(255)),
    Column('game_id', Integer, ForeignKey("games.id")),
)


def map_model_to_tables():
    mapper(Developer, developer_table, properties={
        '_Developer__developer_name': developer_table.c.name,
    })

    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id'            : games_table.c.id,
        '_Game__game_title'         : games_table.c.game_title,
        '_Game__price'              : games_table.c.game_price,
        '_Game__release_date'       : games_table.c.release_date,
        '_Game__description'        : games_table.c.game_description,
        '_Game__image_url'          : games_table.c.game_image_url,
        '_Game__website_url'        : games_table.c.game_website_url,
        '_Game__publisher'          : relationship(Publisher),
        '_Game__genres'             : relationship(Genre, secondary=game_genres_table),
        # '_Game__categories'       : relationship(Category, secondary=game_category_table),
        '_Game__developer'          : relationship(Developer),
        '_Game__achievements'       : games_table.c.achievements,
        '_Game__recommendations'    : games_table.c.recommendations,
        '_Game__notes'              : games_table.c.notes,
        '_Game__windows'            : games_table.c.windows,
        '_Game__apple'              : games_table.c.apple,
        '_Game__linux'              : games_table.c.linux,
        '_Game__average_rating'     : games_table.c.average_rating,
        '_Game__reviews'            : relationship(Review),
        '_Game__trailers'           : relationship(Trailer),
        '_Game__screenshots'        : relationship(Screenshot),
    })

    mapper(Trailer, trailer_table, properties = {
        '_Trailer__link'            : trailer_table.c.link,
        '_Trailer__game'            : relationship(Game, back_populates='_Game__trailers'),    
    })
    
    mapper(Screenshot, screenshot_table, properties={
        '_Screenshot__link'         : screenshot_table.c.link,
        '_Screenshot__game'         : relationship(Game, back_populates='_Game__screenshots'),
    })

    mapper(Review, review_table, properties={
        '_Review__game'             : relationship(Game, back_populates='_Game__reviews'),
        '_Review__user'             : relationship(User, back_populates="_User__reviews"),
        '_Review__comment'          : review_table.c.comment, 
        '_Review__rating'           : review_table.c.rating, 
    })
    
    mapper(User, user_table, properties={
        '_User__username'           : user_table.c.name,
        '_User__password'           : user_table.c.password,
        '_User__profile'            : relationship(Profile),
        '_User__reviews'            : relationship(Review),
        '_User__favourite_games'    : relationship(Favourites),
        '_User__wishlist'           : relationship(Wishlist),
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name'        : genres_table.c.name,
    })
    
    mapper(Wishlist, wishlist_table, properties={
        '_Wishlist__list_of_games'  : relationship(Game, secondary = wishlist_game_table),
    })
    
    mapper(Favourites, favourites_table, properties={
        '_Favourites__list_of_games'  : relationship(Game, secondary = favourites_game_table),
    })
    """
    mapper(Category, category_table, properties={
        '_Category__category_name' : category_table.c.name,
    })"""
    
    mapper(Profile, profile_table, properties={
        '_Profile__description'     : profile_table.c.description,
        '_Profile__show_favourites' : profile_table.c.show_favourites,
        '_Profile__show_wishlist'   : profile_table.c.show_wishlist,
        '_Profile__show_comments'   : profile_table.c.show_comments,
    })
