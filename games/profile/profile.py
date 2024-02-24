from flask import Blueprint, render_template, session, redirect, url_for

from games.profile import services
import games.adapters.repository as repo

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import NumberRange

from wtforms.widgets import TextArea
from games.authentication.authentication import login_required
from games.authentication.services import UserNotFound

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile/<user_name>', methods=['GET'])
def profile(user_name):
    try:
        user = services.get_user(repo.repo_instance, user_name)
        favourites = services.get_favourites(repo.repo_instance, user)
        wishlist = services.get_wishlist(repo.repo_instance, user)
        comments = services.get_comments(repo.repo_instance, user)
    except UserNotFound:
        return redirect(url_for('auth_bp.login'))

    return render_template('user_page/user_page.html', user=user, favourites=favourites, wishlist=wishlist,
                           comments=comments)


@login_required
@profile_blueprint.route("/settings/profile", methods=["GET", "POST"])
def settings():
    form = SettingsForm()

    if form.is_submitted():
        services.update_profile(repo.repo_instance, form.description.data, form.show_favourites.data,
                                form.show_wishlist.data, form.show_comments.data, session['user_name'])
        return redirect(url_for("profile_bp.profile", user_name=session['user_name']))
        pass
    try:
        settings_values = services.get_current_settings(repo.repo_instance, session['user_name'])
    except UserNotFound:
        return redirect(url_for("auth_bp.login"))
    return render_template("user_page/settings.html", form=form, settings=settings_values)


class SettingsForm(FlaskForm):
    description = StringField("Description", widget=TextArea())
    show_favourites = BooleanField("Show Favourites")
    show_wishlist = BooleanField("Show Wishlist")
    show_comments = BooleanField("Show Comments")
    submit = SubmitField("Submit")
