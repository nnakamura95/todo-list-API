from django.test import TestCase
from user.models import CustomUser
from user.user_email_utility import UserEmailUtility
import json


class TestCustomUserManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(id=1, email='user@example.com', password='test123', first_name='User',
                                                  last_name='One',
                                                  is_active=True, is_staff=False)
        cls.superuser = CustomUser.objects.create_superuser(id=2, email='suepruser@example.com', password='test123',
                                                            first_name='Superuser',
                                                            last_name='One',
                                                            is_active=True, is_staff=True, is_superuser=True)

    def test_create_user(self):
        user = CustomUser.objects.get(id=1)

        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("test123"))
        self.assertEqual(user.first_name, "User")
        self.assertEqual(user.last_name, "One")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(str(user), "user@example.com")

    def test_create_superuser(self):
        superuser = CustomUser.objects.get(id=2)

        self.assertEqual(superuser.email, "suepruser@example.com")
        self.assertTrue(superuser.check_password("test123"))
        self.assertEqual(superuser.first_name, "Superuser")
        self.assertEqual(superuser.last_name, "One")
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(str(superuser), "suepruser@example.com")


class TestUserRegistrationView(TestCase):
    def test_post_request_method(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/user/register/', {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "One",
            "password": "test123"
        })

        self.assertEqual(response.status_code, 201)

    def test_post_request_fail(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/user/register/', {
            "email": "",
            "first_name": "Test",
            "last_name": "One",
            "password": "test123"
        })

        self.assertEqual(response.status_code, 400)


class TestActivateUserAccountView(TestCase):

    def test_user_account_activation(self):
        user_register = self.client.post('http://127.0.0.1:8000/api/v1/user/register/', {
            "email": "user@example.com",
            "first_name": "Test",
            "last_name": "One",
            "password": "test123"
        })
        user_email_utility = UserEmailUtility()
        user_email_utility.generate_activation_code()
        user_email_utility.send_activation_code("user@example.com")
        otp = user_email_utility.get_activation_code()
        user_activate = self.client.post('http://127.0.0.1:8000/api/v1/user/activate/', {
            "email": "user@example.com",
            "activation_code": f"{otp}"
        })
        user = CustomUser.objects.get(email="user@example.com")
        response_message = json.loads(user_activate.content.decode('UTF-8'))

        self.assertEqual(user_register.status_code, 201)
        self.assertEqual(user_activate.status_code, 200)
        self.assertEqual(response_message, "The account was successfully activated")
        self.assertEqual(str(user), "user@example.com")

    def test_not_existing_user(self):
        user_email_utility = UserEmailUtility()
        user_email_utility.generate_activation_code()
        user_email_utility.send_activation_code("user@example.com")
        otp = user_email_utility.get_activation_code()
        user_activate = self.client.post('http://127.0.0.1:8000/api/v1/user/activate/', {
            "email": "user@example.com",
            "activation_code": f"{otp}"
        })
        response_message = json.loads(user_activate.content.decode('UTF-8'))

        self.assertEqual(user_activate.status_code, 400)
        self.assertEqual(response_message, "User does not exist")

    def test_invalid_user_account_activation(self):
        user_register = self.client.post('http://127.0.0.1:8000/api/v1/user/register/', {
            "email": "user@example.com",
            "first_name": "Test",
            "last_name": "One",
            "password": "test123"
        })
        user_activate = self.client.post('http://127.0.0.1:8000/api/v1/user/activate/', {
            "email": "user@example.com",
            "activation_code": "",
        })
        response_message = json.loads(user_activate.content.decode('UTF-8'))

        self.assertEqual(user_activate.status_code, 400)
        self.assertEqual(response_message, "Error has occurred during validation")

    def test_otp_invalid_or_expired(self):
        user_register = self.client.post('http://127.0.0.1:8000/api/v1/user/register/', {
            "email": "user@example.com",
            "first_name": "Test",
            "last_name": "One",
            "password": "test123"
        })
        user_activate = self.client.post('http://127.0.0.1:8000/api/v1/user/activate/', {
            "email": "user@example.com",
            "activation_code": "123456",
        })

        self.assertEqual(user_activate.status_code, 500)
        self.assertEqual(user_activate.data["detail"], "The activation code is invalid or expired")


class TestCustomTokenObtainPairView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = CustomUser.objects.create_user(id=1, email='user@example.com', password='test123',
                                                   first_name='User',
                                                   last_name='One',
                                                   is_active=True, is_staff=False)
        cls.user2 = CustomUser.objects.create_user(id=2, email='user1@example.com', password='test123',
                                                   first_name='User',
                                                   last_name='One',
                                                   is_active=False, is_staff=False)

    def test_obtain_access_and_refresh_token(self):
        user_login_info = self.client.post('http://127.0.0.1:8000/api/v1/user/login/', {
            "email": "user@example.com",
            "password": "test123"
        })

        self.assertEqual(user_login_info.status_code, 200)

    def test_in_active_user(self):
        user_login_info = self.client.post('http://127.0.0.1:8000/api/v1/user/login/', {
            "email": "user1@example.com",
            "password": "test123"
        })

        self.assertEqual(user_login_info.status_code, 406)


class TestBlackListTokenView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = CustomUser.objects.create_user(id=1, email='user@example.com', password='test123',
                                                   first_name='User',
                                                   last_name='One',
                                                   is_active=True, is_staff=False)

    def test_user_logout(self):
        user_login_info = self.client.post('http://127.0.0.1:8000/api/v1/user/login/', {
            "email": "user@example.com",
            "password": "test123"
        })
        refresh_token = user_login_info.data["refresh"]
        user_logout = self.client.post('http://127.0.0.1:8000/api/v1/user/logout/', {
            "refresh": f"{refresh_token}"
        })
        response_message = json.loads(user_logout.content.decode('UTF-8'))

        self.assertEqual(response_message, "User successfully logout: refresh token was added to black list")
        self.assertEqual(user_logout.status_code, 205)

    def test_invalid_token(self):
        user_login_info = self.client.post('http://127.0.0.1:8000/api/v1/user/login/', {
            "email": "user@example.com",
            "password": "test123"
        })
        user_logout = self.client.post('http://127.0.0.1:8000/api/v1/user/logout/', {
            "refresh": "123456789abcdefg"
        })
        response_message = json.loads(user_logout.content.decode('UTF-8'))

        self.assertEqual(response_message, "Invalid token")
        self.assertEqual(user_logout.status_code, 400)

