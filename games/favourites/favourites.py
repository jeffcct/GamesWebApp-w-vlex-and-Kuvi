from flask import Blueprint, render_template, request, redirect, url_for, session, abort
import games.adapters.repository as repo
import games.favourites.services as services
from games.authentication.authentication import login_required
from games.authentication.services import UserNotFound


favourites_blueprint = Blueprint('favourites_bp', __name__)


"""Fetching the user's favourite games"""


@favourites_blueprint.route("/favourites")
@login_required
def favourites():
    try:
        user = services.get_user(session['user_name'], repo.repo_instance)
        user_favourites = services.get_favourites(user, repo.repo_instance)
        return render_template('favourites/favourites.html', games=user_favourites, button_text="Remove from Favourites")
    except UserNotFound:
        return redirect(url_for('auth_bp.login'))
    # user = services.get_user(session['user_name'])
    # return render_template('favourites/favourites.html', games=user.favourite_games, button_text="Favourites")


"""Fetching the info from the button"""


@favourites_blueprint.route("/favourite", methods=['GET', 'POST'])
@login_required
def add_favourite():
    user = services.get_user(session['user_name'], repo.repo_instance)  # fetch user based on session name

    game_id = int(request.form.get("fav_game"))
    game = services.get_game(repo.repo_instance, game_id)  # get game based on game_id collected from the post form

    services.add_favourite(user, game, repo.repo_instance)  # invoke user object function to add game

    return redirect(url_for('favourites_bp.favourites'))  # send user to the profile page

    # user = services.get_user(session['user_name'])   # fetch user based on session name
    # game_id = int(request.form.get("fav_game"))
    # game = services.get_game(game_id)  # get game based on game_id collected from the post form
    # user.add_favourite_game(game)  # invoke user object function to add game
    # return redirect(url_for('favourites_bp.favourites'))  # send user to the profile page


@favourites_blueprint.route("/remove-favourite", methods=['GET', 'POST'])
@login_required
def remove_favourite():
    user = services.get_user(session['user_name'], repo.repo_instance)   # fetch user based on session name
    # user_favourites = services.get_favourites(user)

    game_id = int(request.form.get("remove_favourite"))
    game = services.get_game(repo.repo_instance, game_id)  # get game based on game_id collected from the post form

    services.remove_favourite_game(user, game, repo.repo_instance)  # invoke user object function to add game
    return redirect(url_for('favourites_bp.favourites'))  # send user to the profile page


