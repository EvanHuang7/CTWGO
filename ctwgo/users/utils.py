import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from ctwgo import mail


############################################################################################

# function for saving image to folder.
def save_picture(form_picture):
	# change file name to a random hash number.
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext

	# scale down the image and save the image to folder
	picture_path = os.path.join(current_app.root_path,'static/profile_pics', picture_fn)
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


############################################################################################

# function for sending an email
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='robotcs1987@gmail.com', recipients=[user.email])

	# "_external=True" is to get absolute URL rather than relative URL.
	msg.body = f''' To  reset your password, vist the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''

	mail.send(msg)