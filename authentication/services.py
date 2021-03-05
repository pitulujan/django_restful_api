from .errors import InvalidId
from .schemas import UserSchema
from bson.objectid import ObjectId
from .mongo import Repository
from .mongo.mongo import MongoRepository


class Service:
    def __init__(self, repo_client=Repository(adapter=MongoRepository)):
        self.repo_client = repo_client

    def find_user(self, username=None, _id=None):
        if username is not None:
            user = self.repo_client.find_one({"username": username}, "users")
            if user is not None:
                user["_id"] = str(user["_id"])
                user = UserSchema().load(user)
        else:
            user = self.repo_client.find_one({"_id": ObjectId(_id)}, "users")
            if user is not None:
                user["_id"] = str(user["_id"])
                user = UserSchema().load(user)
        return user
