#below means "from user.py file, import the User class defined therein" - possible bc user.py is in the same directory as this file.

# safe_str_cmp means "safe string compare" - so instead of using this_str == that_str, you do safe_str_cmp(this_str, that_str) - used because
# sometimes different strings can have different encodings (ASCII, etc) and this accounts for that.
from models.user import UserModel
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
	user = UserModel.find_by_username(username)
	if user and safe_str_cmp(user.password, password):
		return user

#identity function here is specific to flask-JWT, whitch takes in a payload (the contents of a JWT token), and then
# you extract the user ID from that payload.
def identity(payload):
	user_id = payload['identity']
	return UserModel.find_by_id(user_id)
