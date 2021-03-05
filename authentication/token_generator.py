import datetime
import jwt
from django.conf import settings


def generate_access_token(user_id):

    access_token_payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.PRIVATE_KEY, algorithm='RS256').decode('utf-8')
    return access_token


def generate_refresh_token(user_id):
    refresh_token_payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.PRIVATE_KEY, algorithm='RS256').decode('utf-8')

    return refresh_token