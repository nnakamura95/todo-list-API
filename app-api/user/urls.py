from django.urls import path
from .views import UserRegistrationView, BlackListTokenView, ActivateUserAccountView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register_user'),
    path('activate/', ActivateUserAccountView.as_view(), name='activate_account'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', BlackListTokenView.as_view(), name='blacklist'),
]
