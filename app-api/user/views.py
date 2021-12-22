from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, CustomTokenPairSerializer, InActiveUser
from .user_email_utility import UserEmailUtility
from .models import CustomUser

# Global variable for user email utility
user_email_utility = UserEmailUtility()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        register_serializer = UserRegistrationSerializer(data=request.data)
        if register_serializer.is_valid():
            user_email_utility.generate_activation_code()
            user_email_utility.send_activation_code(register_serializer.validated_data.get("email"))
            new_user = register_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = CustomUser.objects.get(email=request.data["email"])
        except ObjectDoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)

        if user_email_utility.verify_code(request.data["activation_code"]):
            user.is_active = True
            user.save()
            return Response("The account was successfully activated", status=status.HTTP_200_OK)
        return Response("Error has occurred during validation", status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenViewBase):

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            raise InActiveUser()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class BlackListTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("User successfully logout: refresh token was added to black list",
                            status=status.HTTP_205_RESET_CONTENT)
        except Exception as invalid_token:
            return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)
