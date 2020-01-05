from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,jsonify)
from flask_login import current_user, login_required
from ctwgo import db
from ctwgo.models import Post, Comment, Like, User
from ctwgo.posts.forms import PostForm
from ctwgo.posts.utils import save_picture


posts = Blueprint('posts', __name__)


############################################################################################
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		# If there is a picture in new post
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			post = Post(title=form.title.data, content=form.content.data, author=current_user, picture_file=picture_file)
		else:
			post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'light')
		return redirect(url_for('main.home'))

	return render_template('create_post.html', title='New Post',form=form, legend='New Post')


############################################################################################
@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
	# if the post with this ID does not exist, then return a 404. 
	post = Post.query.get_or_404(post_id)
	comments = Comment.query.filter_by(post_id=post_id).all()

	if post.picture_file is not None:
		picture_file = url_for('static', filename='post_pics/' + post.picture_file)
		return render_template('post.html', title=post.title, post=post, comments=comments,picture_file=picture_file)
	else:
		return render_template('post.html', title=post.title, post=post, comments=comments)


############################################################################################
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	# if the post with this ID does not exist, then return a 404. 
	post = Post.query.get_or_404(post_id)

	if post.author != current_user:
		abort(403)
	form = PostForm()

	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			post.picture_file = picture_file
		db.session.commit()
		flash('Your post has been updated!', 'light')
		return redirect(url_for('posts.post', post_id=post.id))

	# We want the original title and original contetn display in the update post page.
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post',form=form, legend='Update Post')



############################################################################################
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	# if the post with this ID does not exist, then return a 404. 
	post = Post.query.get_or_404(post_id)
	comments = Comment.query.filter_by(post_id=post_id).all()
	likes = Like.query.filter_by(post_id=post_id).all()

	if post.author != current_user:
		abort(403)
	db.session.delete(post)

	for comment in comments:
		db.session.delete(comment)

	for like in likes:
		db.session.delete(like)
		
	db.session.commit()
	flash('Your post has been deleted!', 'light')
	return redirect(url_for('main.home'))



############################################################################################
@posts.route("/post/<int:post_id>/<int:user_id>/like", methods=['GET', 'POST'])
@login_required
def like_post(post_id,user_id):
	item = Like.query.filter_by(user_id=user_id).filter_by(post_id=post_id).first()
	if item is None:
		like = Like(user_id=user_id, post_id=post_id, like=True)
		db.session.add(like)
		db.session.commit()
	else:
		item.like = True
		db.session.commit()
	return redirect(url_for('posts.post', post_id=post_id))
	

@posts.route("/post/<int:post_id>/<int:user_id>/dislike", methods=['GET', 'POST'])
@login_required
def dislike_post(post_id,user_id):
	item = Like.query.filter_by(user_id=user_id).filter_by(post_id=post_id).first()
	if item is None:
		like = Like(user_id=user_id, post_id=post_id, like=False)
		db.session.add(like)
		db.session.commit()
	else:
		item.like = False
		db.session.commit()
	return redirect(url_for('posts.post', post_id=post_id))


############################################################################################
@posts.route("/post/search/<string:searching>", methods=['GET', 'POST'])
def search_posts(searching):
	page = request.args.get('page', 1, type=int)

	if request.method == 'POST':
		req = request.form
		searching = req["searching"]

		if searching == "":
			flash('Please enter some key words of title!', 'light')
			return redirect(url_for('main.home'))


		posts = Post.query.filter(Post.title.contains(searching))\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=4)

		return render_template('search_posts.html', title='Search Post', posts=posts, searching=searching)
	
	if request.method == 'GET':
		posts = Post.query.filter(Post.title.contains(searching))\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=4)
		return render_template('search_posts.html', title='Search Post', posts=posts, searching=searching)

