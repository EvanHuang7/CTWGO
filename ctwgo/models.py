from flask import current_app
from ctwgo import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



# Create a fucntion for reloading the user from the user ID.
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


############################################################################################
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)

	# define a one to many relationship between user and post, user and comment.
	posts = db.relationship('Post', backref='author', lazy=True)
	comments = db.relationship('Comment', backref='author', lazy=True)


	# Generate a token(for reseting password with an email link).
	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')


	# Validate a token(for reseting password with an email link).
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	# check the user if like this post in database.
	def check_like(self, post_id):
		item = Like.query.filter_by(user_id=self.id).filter_by(post_id=post_id).first()
		if item is None:
			return False
		else:
			return item.like

	# calculate the number of likes for user's all posts in database.
	def rank_like(self):
		like_number = 0
		posts = Post.query.filter_by(user_id=self.id).all()
		for post in posts:
			likes = Like.query.filter_by(post_id=post.id).filter_by(like=True).all()
			like_number += len(likes)
		return self.username,like_number

	# calculate the number of all posts of user in database.
	def rank_post(self):
		posts = Post.query.filter_by(user_id=self.id).all()
		return len(posts)

	def __repr__(self):
		return f"User( '{self.username}','{self.email}','{self.image_file}' )"


############################################################################################
class Post(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	picture_file = db.Column(db.String(40), nullable=True)

	# 'user.id', we reference to the table and column name, so use lower case.
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	comments = db.relationship('Comment', backref='post', lazy=True)

	# count likes number for this post.
	def count_like(self):
		likes = Like.query.filter_by(post_id=self.id).filter_by(like=True).all()
		return len(likes)

	def __repr__(self):
		return f"Post( '{self.title}','{self.date_posted}' )"


############################################################################################
class Comment(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

	def __repr__(self):
		return f"Comment( '{self.user_id}','{self.post_id}','{self.date_posted}' )"


############################################################################################
class Like(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	post_id = db.Column(db.Integer, nullable=False)
	like = db.Column(db.Boolean, nullable=False)

	def __repr__(self):
		return f"Like( '{self.user_id}','{self.post_id}','{self.like}' )"

