from rest_framework.views import APIView
from rest_framework.response import Response
from .services import Service
from rest_framework import exceptions

conn = Service()


class GetTasks(APIView):

    def get(self, request, task_id=None):
        print(task_id)
        if task_id is None:
            tasks = conn.find_task()
        else:
            tasks = conn.find_task(_id=task_id)
            if len(tasks) == 0:
                raise exceptions.NotFound("Id not found")
        return Response(tasks)