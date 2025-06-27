from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """
        Form for creating or updating a blog post.

        Fields:
            - title: Required. Title of the blog post.
            - content: Required. Body content of the post (textarea).
            - submit: Submit button labeled 'Post'.
    """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')