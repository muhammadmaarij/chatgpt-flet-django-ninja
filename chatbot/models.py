# chatbot/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='chatbot_user_set',  # Change related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='chatbot_user_set',  # Change related name
        blank=True,
    )
