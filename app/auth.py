
from urllib.request import HTTPBasicAuthHandler


auth = HTTPBasicAuthHandler()

users = {
    "admin": "securepassword"  # Store hashed passwords in production!
}


@auth.verify_password
def verify(username, password):
    if username in users and users[username] == password:
        return username
