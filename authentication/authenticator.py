import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
import base64
from .services import Service

conn = Service()


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class SafeBasicOrJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header is None:
            raise exceptions.AuthenticationFailed('Basic of JWT Auth required')

        try:
            token_type, _, credentials = auth_header.partition(' ')
        except Exception as inst:  
            raise exceptions.AuthenticationFailed(str(inst))
    
        if token_type.lower() == "basic":
            username, password = base64.b64decode(credentials).decode().split(':')
            user = conn.find_user(username)
            if user is None or not user.check_password(password):
                raise exceptions.AuthenticationFailed("Wrong username or password")
            return (user, None)

        elif token_type.lower() == "bearer":

            try:
                payload = jwt.decode(
                    credentials, settings.PUBLIC_KEY, algorithms=['RS256'])

            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('access_token expired')
            except IndexError:
                raise exceptions.AuthenticationFailed('Token prefix missing')
            except jwt.DecodeError:
                raise exceptions.AuthenticationFailed('Decode Error')

            user = conn.find_user(_id=payload["user_id"])
            if user is None:
                raise exceptions.AuthenticationFailed('User not found')

            self.enforce_csrf(request)
            return (user, None)

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
