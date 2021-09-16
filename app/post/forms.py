from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, FileField
from wtforms.validators import DataRequired


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Say something:', validators=[DataRequired()])
    tag = StringField('Add tags:', validators=[DataRequired()])
    file = FileField('Add image to your post:')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = TextAreaField('Write your comment:', validators=[DataRequired()])
    parentId = HiddenField()
    submit = SubmitField('Submit')


class MyForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')
