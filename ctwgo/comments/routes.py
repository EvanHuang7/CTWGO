from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from ctwgo import db
from ctwgo.models import Post, Comment
from ctwgo.comments.forms import CommentForm


comments = Blueprint('comments', __name__)

############################################################################################
# we need "/post/<int:post_id>".
@comments.route("/post/<int:post_id>/comment/new", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
	form = CommentForm()
	if form.validate_on_submit():
		post = Post.query.get_or_404(post_id)
		comment = Comment( content=form.content.data, author=current_user, post=post)
		db.session.add(comment)
		db.session.commit()
		flash('Your comment has been created!', 'light')
		return redirect(url_for('posts.post', post_id=post.id))

	return render_template('create_comment.html', title='New Comment',form=form, legend='New Comment')


############################################################################################
@comments.route("/post/<int:post_id>/<int:comment_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_comment(post_id, comment_id):
	# if the post with this ID does not exist, then return a 404. 
	comment = Comment.query.get_or_404(comment_id)

	if comment.author != current_user:
		abort(403)
	db.session.delete(comment)
	db.session.commit()
	flash('Your comment has been deleted!', 'light')
	return redirect(url_for('posts.post', post_id=post_id))