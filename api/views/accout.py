import uuid
from datetime import datetime

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from api.extension.mixins import DigCreateModelMixin
import api.extension.return_code
from api import models
from api.serializers.accout import RegisterSerializer,AuthSerializer
from rest_framework.viewsets import GenericViewSet

class registerView(DigCreateModelMixin,GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.validated_data.pop('confirm_password')
        serializer.save()


class AuthView(APIView):
    '''用户登录'''

    authentication_classes = []
    permission_classes = []
    def post(self,request):
        serializer = AuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"code":api.extension.return_code.VALIDATE_ERROR,"detail":serializer.errors})

        username = serializer.validated_data.get('username')
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')

        user_object = models.UserInfo.objects.filter(Q(Q(username=username) | Q(phone=phone)),password=password).first()
        if not user_object:
            return Response({"code":api.extension.return_code.VALIDATE_ERROR,"error":"用户名或密码错误"})
        # 生成token
        token = str(uuid.uuid4())
        user_object.token = token

        # 设置token有效期：当前时间 + 2周
        user_object.token_time = datetime.datetime.now() + datetime.timedelta(weeks=2)
        user_object.save()

        return Response({"code":api.extension.return_code.SUCCESS,"data":{"token":token}})