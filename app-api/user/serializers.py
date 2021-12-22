from django.contrib.auth.models import update_last_login
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        if first_name is None:
            raise ValueError(_("First name must be set"))
        if last_name is None:
            raise ValueError(_("Last name must be set"))
        user.save()
        return user


class InActiveUser(AuthenticationFailed):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "User is not active, please activate your account"
    default_code = 'user_is_inactive'


class CustomTokenPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise InActiveUser()

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
