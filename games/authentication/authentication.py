from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator
from games.authentication import services

import games.adapters.repository as repo

from functools import wraps

authentication_blueprint = Blueprint('auth_bp', __name__)


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    error_message = None
    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data,
                              form.password.data,
                              repo.repo_instance)
            return redirect(url_for('auth_bp.login'))
        except services.NameNotUniqueError:
            error_message = "User already exists!"

    return render_template('authentication/login.html',
                           form=form,
                           error_msg=error_message,
                           type="Register")


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_msg = None
    if form.validate_on_submit():
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)

            services.auth_user(user.username, form.password.data, repo.repo_instance)

            session.clear()
            session['user_name'] = user.username
            # return redirect(url_for('home_bp.home'))
            let_user = services.get_user(session['user_name'], repo.repo_instance)
            return redirect(url_for('home_bp.home'))

        except services.AuthenticationError:
            error_msg = "Password Incorrect!"
        except services.UserNotFound:
            error_msg = "Username Incorrect!"
    return render_template('authentication/login.html',
                           form=form,
                           handler_url=url_for('auth_bp.login'),
                           error_msg=error_msg,
                           type="Login")


@authentication_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('auth_bp.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    def __init__(self, msg=None):
        if not msg:
            msg = 'Your password must be 8 characters long, have an uppercase, lowercase and a digit'
        self.message = msg

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message="Please enter a username")])
    password = PasswordField('Password', [
        DataRequired(message="Please enter a password")
    ])
    submit = SubmitField('Login')
