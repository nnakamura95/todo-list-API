from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('User must have an email'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password == '':
            raise ValueError(_('Password can not be empty'))
        if password is None:
            raise ValueError(_('Password can not be Null value'))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must be is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must be is_superuser=True."))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_("Superuser must be is_active=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
