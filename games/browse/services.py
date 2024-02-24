from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num = int(round(num / 1000.0, 1))
    return '{}{}'.format(num, ['', 'K', 'M'][magnitude])


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def extract_games(games):
    game_dicts = []
    for game in games:
        game_dict = {
            'game_id'           : game.game_id,
            'title'             : game.title,
            'release_date'      : game.release_date,
            'image_url'         : game.image_url,
            'price'             : game.price,
            'date'              : game.release_date,
            'publisher'         : game.publisher,
            'description'       : game.description,
            'recommendations'   : human_format(game.recommendations),
            'achievements'      : human_format(game.achievements),
            'windows'           : game.windows,
            'apple'             : game.apple,
            'linux'             : game.linux,
            'genres'            : game.genres,
            # #'categories'        : game.categories,
            'reviews'           : game.reviews,
            'average_rating'    : round(game.average_rating, 2),
            'rounded_rating'    : int(round(game.average_rating, 0)),
        }
        game_dicts.append(game_dict)
    return game_dicts


def get_games(repo: AbstractRepository):  # be DRY
    games = repo.get_games()
    return games


def get_games_by_genre(repo: AbstractRepository, genre_name: str):
    genre = Genre(genre_name)
    games_by_genre = repo.get_games_by_genre(genre)
    return games_by_genre


def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    new_genres = []
    for genre in genres:
        new_genres.append(genre)
    return new_genres
