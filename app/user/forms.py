from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import ValidationError, DataRequired, Length
from app.user_models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = StringField('About me',
                             validators=[Length(min=0, max=140)])
    avatar = FileField('Avatar')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class MessageForm(FlaskForm):
    message = TextAreaField('Write a message:', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Send')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    style = {'class': 'ourClasses', 'style': 'width:30%;'}
    username = StringField('Search for user:', validators=[DataRequired()], render_kw=style)
    submit = SubmitField('Search')
