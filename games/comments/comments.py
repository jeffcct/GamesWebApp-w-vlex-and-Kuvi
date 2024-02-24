from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import NumberRange

from wtforms.widgets import TextArea


from password_validator import PasswordValidator
from games.authentication import services

import games.adapters.repository as repo

class CommentsForm(FlaskForm):
    rating = StringField('Rating', render_kw={"placeholder": 0} ,validators=[NumberRange(min=1, max=5)])
    comment = StringField('Comment', widget=TextArea())
    submit = SubmitField('Register')