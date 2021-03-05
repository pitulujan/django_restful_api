from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import exceptions
from .token_generator import generate_access_token, generate_refresh_token


class GetToken(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):

        response = Response()
        access_token = generate_access_token(request.user.id)
        refresh_token = generate_refresh_token(request.user.id)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': {'id':request.user.id,'username':request.user.username}
        }

        return response