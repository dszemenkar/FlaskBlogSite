from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	picture = FileField('Picture', validators=[FileAllowed(['jpg','png'])])
	text = TextAreaField('Text', validators=[DataRequired()])
	submit = SubmitField('Post')