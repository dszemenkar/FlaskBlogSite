from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from blogsite import db
from blogsite.models import BlogPost
from blogsite.posts.forms import BlogPostForm
from blogsite.posts.picture_handler import add_pic

blogposts = Blueprint('blogposts', __name__)

@blogposts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	form = BlogPostForm()

	if form.validate_on_submit():
		filename = 'default.png'
		if form.picture.data:
			filename = add_pic(form.picture.data)

		blogpost = BlogPost(title=form.title.data,
							picture=filename,
							text=form.text.data,
							user_id=current_user.id)
		db.session.add(blogpost)
		db.session.commit()
		return redirect(url_for('core.index'))
	return render_template('create_post.html', form=form)

@blogposts.route('/<int:blogpost_id>')
def blogpost(blogpost_id):
	blogpost = BlogPost.query.get_or_404(blogpost_id)
	return render_template('blogpost.html', title=blogpost.title, date=blogpost.date,post=blogpost)

@blogposts.route('/<int:blogpost_id>/update', methods=['GET', 'POST'])
def update(blogpost_id):
	blogpost = BlogPost.query.get_or_404(blogpost_id)
	if blogpost.author != current_user:
		abort(403)

	form = BlogPostForm()
	if form.validate_on_submit():
		filename = 'default.png'
		if form.picture.data:
			filename = add_pic(form.picture.data)

		blogpost.title = form.title.data
		blogpost.picture = filename
		blogpost.text = form.text.data
		db.session.add(blogpost)
		db.session.commit()
		return redirect(url_for('blogposts.blogpost', blogpost_id=blogpost.id))

	elif request.method == 'GET':
		form.title.data = blogpost.title
		form.text.data = blogpost.text

	return render_template('create_post.html', title='Update post', form=form)

@blogposts.route('/<int:blogpost_id>/delete', methods=['GET', 'POST'])
def delete(blogpost_id):
	blogpost = BlogPost.query.get_or_404(blogpost_id)
	if blogpost.author != current_user:
		abort(403)

	db.session.delete(blogpost)
	db.session.commit()
	return redirect(url_for('core.index'))