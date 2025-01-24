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