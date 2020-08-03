from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from habit_app.models import User, Habit
from wtforms.widgets import html5 as h5widgets


# AUTH FROMS

class RegistrationForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    remember = BooleanField('Rememeber me')
    submit = SubmitField('Login')



# HABIT FORMS

class HabitForm(FlaskForm):
    activity = StringField(
        'Activity',
        validators=[DataRequired(), Length(max=100)]
    )
    time_spent = IntegerField(
        'Time Spent (in minutes)',
        validators=[DataRequired()],
        widget=h5widgets.NumberInput(min=0)
    )
    description = TextAreaField('Description (optional)')
    submit = SubmitField('Add activity')