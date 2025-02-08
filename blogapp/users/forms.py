from flask_login import current_user
from flask_migrate import current
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import PasswordField, StringField, SubmitField, ValidationError, validators
from wtforms.validators import DataRequired, Email, EqualTo

from blogapp.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("UserName", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("pass_confirm", message="Password must match"),
        ],
    )
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has been registered already!")

class UpdateUserForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("UserName", validators=[DataRequired()])
    picture = FileField(
        "Update profile picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")