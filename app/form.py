from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class RegisterForm(FlaskForm):

    company_name = StringField(
        "Company Name",
        validators=[DataRequired("company name required"), Length(min=2, max=100)],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired("email address required."),
            Email("enter a valid email address."),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Password is required"),
            Length(min=6, message="Password must be minimum of 6 characters."),
        ],
    )

    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired("Confirm your password."),
            EqualTo("password", "Password must match."),
        ],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired("Email address required."),
            Email("Enter a valid email address."),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Password is required"),
        ],
    )

    submit = SubmitField("log in")


class CreateFlagForm(FlaskForm):

    key = StringField(
        "flag key",
        validators=[
            DataRequired("flag key required"),
            Length(min=3, max=64),
            Regexp(
                r"^[a-bA-B0-9_\-]",
                message="Key can only contain letters, numbers, underscores, and hyphens.",
            ),
        ],
    )

    name = StringField(
        "flag name", validators=[DataRequired("name required"), Length(max=100)]
    )
    description = StringField("description", validators=[Length(max=255)])
    is_enabled = BooleanField("Enable immediately")
    submit = SubmitField("Create Flag")


class ToggleFlagForm(FlaskForm):

    submit = SubmitField("Toggle")
