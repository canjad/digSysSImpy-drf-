import datetime
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api.extension import return_code
from api import models

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token")
        if not token:
            raise AuthenticationFailed(return_code.AUTH_FAILED)
        user_object = models.UserInfo.objects.filter(token=token).first()
        if not user_object:
            raise AuthenticationFailed(return_code.AUTH_FAILED)
        # token是否过期
        current_time = datetime.datetime.now()
        if datetime.datetime.now() > user_object.token_time:
            raise AuthenticationFailed(return_code.AUTH_FAILED)
        return user_object, token
    def authenticate_header(self, request):
        return 'Bearer realm="API"'
