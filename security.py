# safe_str_cmp is safe in the sense that it comapres even if different strings have different encodings (ASCII, UTF, etc)
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
