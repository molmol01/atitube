from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, DateField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired
from atitube.models import User


class RegisterForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password',
                             validators=[DataRequired(), Length(min=4), EqualTo('password')])
    confirmPassword = PasswordField('confirm password')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(".השם משתמש בשימוש, נסה שם אחר")

    def validate_Email(self, email):
        email = User.query.filter_by(Email=email.data).first()
        if email:
            raise ValidationError(".לאימייל זה קיים חשבון, הכנס אימייל אחר")


class LoginForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('password',
                             validators=[DataRequired(), Length(min=4), EqualTo('password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('log in')


class UpdateAccount(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(".השם משתמש בשימוש, נסה שם אחר")

    def validate_Email(self, Email):
        if Email.data != current_user.Email:
            Email = User.query.filter_by(Email=Email.data).first()
            if Email:
                raise ValidationError(".לאימייל זה קיים חשבון, הכנס אימייל אחר")


class VideoForm(FlaskForm):
    name = StringField('name',
                       validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description')
    video = FileField('Video', validators=[FileRequired()])
    submit = SubmitField('submit')


