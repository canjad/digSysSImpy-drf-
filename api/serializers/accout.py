from django.core.exceptions import ValidationError
from rest_framework import serializers

from api import models


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(label="确认密码", min_length=8, max_length=16, write_only=True)
    password = serializers.CharField(label="密码", min_length=8, max_length=16, write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ['username', "phone", "password", "confirm_password"]



    def validate_username(self, value):
        """
        验证用户名唯一性
        """
        if models.UserInfo.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_phone(self, value):
        """
        验证手机号格式和唯一性
        """
        # 验证手机号格式
        # if not re.match(r'^1[3-9]\d{9}$', value):
        #     raise serializers.ValidationError("手机号格式不正确")

        # 验证手机号唯一性
        if models.UserInfo.objects.filter(phone=value).exists():
            raise serializers.ValidationError("手机号已被注册")

        return value

    def validate_confirm_password(self, value):
        """
        验证两次输入的密码是否一致
        """
        password = self.initial_data.get('password')
        if password and password != value:
            raise serializers.ValidationError("两次输入的密码不一致")
        return value
class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(label="用户名", write_only=True, required=False)
    phone = serializers.CharField(label="手机号", write_only=True, required=False)
    password = serializers.CharField(label="密码", write_only=True)

    def validate_username(self, value):
        username =self.initial_data.get('username')
        phone = self.initial_data.get('phone')
        if not username and not phone:
            raise ValidationError('用户名和手机号必须传一个')
        if username and phone:
            raise ValidationError('用户名和手机号只能传一个')
        return value

