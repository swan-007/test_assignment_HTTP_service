from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, name, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not name:
            raise ValueError("Не указано имя пользователя")
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = "username"
    objects = UserManager()
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.username}"


class FileU(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="file")
    created_data = models.DateTimeField(auto_now_add=True)
    column_file = models.TextField()
    file = models.FileField()
