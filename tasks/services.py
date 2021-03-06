from .errors import InvalidId
from .schemas import TaskSchema
from bson.objectid import ObjectId
from .mongo import Repository
from .mongo.mongo import MongoRepository


class Service:
    def __init__(self, repo_client=Repository(adapter=MongoRepository)):
        self.repo_client = repo_client

    def find_task(self, _id=None):
        if _id is not None:
            try:
                tasks_mongo = self.repo_client.find_one(
                    {"_id": ObjectId(_id)}, "tasks_bucket"
                )
            except:
                raise InvalidId("Not supported Id type")

            if tasks_mongo is not None:
                tasks = [TaskSchema().dump(tasks_mongo)]
            else:
                tasks = []

        else:

            tasks_mongo = self.repo_client.find_all({}, "tasks_bucket")
            tasks = TaskSchema(many=True).dump(tasks_mongo)

        return tasks

    def create_task(self, title, description, done):

        new_task = {
            "title": title,
            "description": description,
            "done": done,
        }
        new_task["_id"] = self.repo_client.create(new_task, "tasks_bucket").inserted_id
        return TaskSchema().dump(new_task)

    def update_task(self, task, task_to_update):
        _id = str(task["_id"])
        records_affected = self.repo_client.update_one(
            {"_id": ObjectId(_id)}, {"$set": task_to_update}, "tasks_bucket"
        )
        task.update(task_to_update)
        return task

    def delete_task(self, task):
        records_affected = self.repo_client.delete(
            {"_id": ObjectId(task["_id"])}, "tasks_bucket"
        )
        if records_affected:
            ret = task
        else:
            ret = {"error": "unknown error"}
        return ret
