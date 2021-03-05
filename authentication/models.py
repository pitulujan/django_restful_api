import random
from django.contrib.auth.hashers import PBKDF2PasswordHasher

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

class User:
    def __init__(self, _id, username, password, admin=False):
        self.username = username
        self.password_hash = password
        self.id = _id
        self.admin = admin
        self.is_authenticated = True

    def set_password(self, password):
        self.password_hash = PBKDF2PasswordHasher().encode(password,''.join(random.choice(ALPHABET) for i in range(16)))

    def check_password(self, password):
        return PBKDF2PasswordHasher().verify(password,self.password_hash)
