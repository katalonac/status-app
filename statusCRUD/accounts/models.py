from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.conf import settings


class UserManager(BaseUserManager):
    """Create and manage users."""

    def create_user(self, first_name, last_name, email,
                    username=None, password=None, is_active=True,
                    is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, first_name, last_name, email,
                         username=None, password=None):
        user = self.create_user(
            first_name,
            last_name,
            email,
            username,
            password,
        )
        user.active = True
        user.staff = True
        user.admin = False
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, 
                         username=None, password=None):
        user = self.create_user(
            first_name,
            last_name,
            email,
            username,
            password
        )
        user.active = True
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model data."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=40, unique=True, null=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # USENAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return "{} {} (@{})".format(self.first_name, self.last_name,
            self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"

        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
