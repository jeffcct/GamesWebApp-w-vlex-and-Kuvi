from flask import Blueprint, render_template, request, redirect, url_for, session, abort
import games.adapters.repository as repo
import games.browse.services as services
import math


browse_blueprint = Blueprint('browse_bp', __name__)


def browse_games(games, template, page = 1):
    games = services.extract_games(games)
    num_games = len(games)
    games_per_page = 50  # Number of games to display per page
    if page * games_per_page > num_games + games_per_page:
        page = 1
    if page < 1:
        page = math.ceil(num_games / games_per_page)
        
    all_genres = services.get_genres(repo.repo_instance)
    start_idx = (page - 1) * games_per_page
    if start_idx > num_games and num_games > 0:
        return abort(404)
    end_idx = min(start_idx + games_per_page, num_games)
    games_on_page = games[start_idx:end_idx]
    
    has_prev = page > 1
    has_next = end_idx < num_games
    
    return render_template(template, games=games_on_page, page=page, has_prev=has_prev, has_next=has_next, genres=all_genres)


@browse_blueprint.route('/games/', methods=['GET'])
def browse_all_games():
    page = request.args.get("page")
    try:
        page = int(page)
    except TypeError:
        page=1
    all_games = services.get_games(repo.repo_instance)
    return browse_games(all_games, 'browse.html', page)


@browse_blueprint.route('/games/<genre_name>', methods=['GET'])
def browse_games_by_genre(genre_name):
    page = request.args.get("page")
    try:
        page = int(page)
    except TypeError:
        page=1
    games = services.get_games_by_genre(repo.repo_instance, genre_name)
    return browse_games(games, 'browse.html', page)

@browse_blueprint.route('/games/<int:page_number>')
def browse_game_page(page_number):
    games = services.get_games(repo.repo_instance)
    return browse_games(games, 'browse.html', page_number)

@browse_blueprint.route('/search/<input>')
def browse_by_query(input):
    page = request.args.get("page")
    try:
        page = int(page)
    except TypeError:
        page=1
    games = services.get_games_by_genre(repo.repo_instance)
    return browse_games(games, 'browse.html', page)