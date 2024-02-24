from flask import Blueprint, render_template, abort, session, redirect, url_for
import games.adapters.repository as repo
import games.game.services as services

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import NumberRange

from wtforms.widgets import TextArea

game_blueprint = Blueprint('game_bp', __name__)


@game_blueprint.route('/game/<int:gameid>', methods=['GET', 'POST'])
def game_description(gameid):
    game = services.get_game(repo.repo_instance, gameid)
    form = CommentsForm()
    error_message = None

    if form.is_submitted():
        try:
            services.add_comment(repo.repo_instance, form.comment.data, form.rating.data, session['user_name'], game)
            return redirect(url_for('game_bp.game_description', gameid=gameid))
        except ValueError:
            error_message = 'Enter a value between 1 and 5'
        

    return render_template('gameDescription/gameDescription.html', game=game, form=form, err_msg=error_message)

        


class CommentsForm(FlaskForm):
    rating = IntegerField("Rating", render_kw={"placeholder": 0}, validators=[NumberRange(min=1, max=5)])
    comment = StringField('Comment', render_kw={"placeholder": "Enter a comment..."}, widget=TextArea())
    submit = SubmitField('Add Comment')