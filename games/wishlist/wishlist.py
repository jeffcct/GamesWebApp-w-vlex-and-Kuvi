from flask import Blueprint, render_template, request, redirect, url_for, session, abort
import games.adapters.repository as repo
import games.wishlist.services as services
from games.authentication.authentication import login_required
from games.domainmodel.model import User, Wishlist
from games.authentication.services import UserNotFound



wishlist_blueprint = Blueprint('wishlist_bp', __name__)


"""
@wishlist_blueprint.route("/wishlist")
@login_required
def wishlist():
    user = services.get_user(session['user_name'], repo.repo_instance)
    wishlist_obj = services.get_wishlist(user)
    wishlist_games = wishlist_obj.list_of_games()
    return render_template('wishlist/wishlist.html', games=wishlist_games, button_text="Wishlist")
"""

@wishlist_blueprint.route("/wishlist")
@login_required
def wishlist():
    try:
        user = services.get_user(session['user_name'], repo.repo_instance)
        # user_wishlist = services.get_wishlist(user)
        # refactored 09/10 for db repo
        user_wishlist = services.get_wishlist(repo.repo_instance, user)
        return render_template('wishlist/wishlist.html', games=user_wishlist, button_text="Remove From Wishlist")
    except UserNotFound:
        return redirect(url_for('auth_bp.login'))


@wishlist_blueprint.route("/add-to-wishlist", methods=['GET', 'POST'])
@login_required
def add_to_wishlist():
    user = services.get_user(session['user_name'], repo.repo_instance)   # fetch user based on session name
    # user_wishlist = services.get_wishlist(user)

    game_id = int(request.form.get("wishlist_game"))
    game = services.get_game(repo.repo_instance, game_id)  # get game based on game_id collected from the post form

    # services.add_to_wishlist(user, game)  # invoke user object function to add game
    # 09/10 changed for db
    services.add_to_wishlist(repo.repo_instance, user, game)  # invoke user object function to add game

    return redirect(url_for('wishlist_bp.wishlist'))  # send user to the profile page


@wishlist_blueprint.route("/remove-from-wishlist", methods=['GET', 'POST'])
@login_required
def remove_from_wishlist():
    user = services.get_user(session['user_name'], repo.repo_instance)   # fetch user based on session name
    # user_wishlist = services.get_wishlist(user)

    game_id = int(request.form.get("remove_from_wishlist"))
    game = services.get_game(repo.repo_instance, game_id)  # get game based on game_id collected from the post form

    # services.remove_from_wishlist(user, game)  # invoke user object function to add game
    # 09/10 changed for db
    services.remove_from_wishlist(repo.repo_instance, user, game)  # invoke user object function to add game

    return redirect(url_for('wishlist_bp.wishlist'))  # send user to the profile page
