from flask import render_template, request, Blueprint, redirect, url_for
from ctwgo.models import Post, User


main = Blueprint('main', __name__)


############################################################################################
@main.route("/")
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)

	# find the post's like rank
	all_users_likes =[]
	users_rank = []
	users = User.query.all()

	# If there is user in database
	if users is not None:
		for user in users:
			all_users_likes.append(user.rank_like())
		# find the users with top 3 post's like 
		for i in range(3):
			best = 'No User'
			max = 0
			index = 0
			for u in range(len(all_users_likes)):
				if all_users_likes[u][1] >= max:
					best = all_users_likes[u][0]
					max = all_users_likes[u][1]
					index = u
			users_rank.append((best,max))
			if all_users_likes != []:
				all_users_likes.pop(index)

	# if no user in database
	else:
		all_users_likes = [('No User', 0), ('No User', 0), ('No User', 0)]

	return render_template('home.html', posts=posts,users_rank=users_rank, no_user='No User')


############################################################################################

@main.route("/about")
def about():
	return render_template('about.html', title='About')


