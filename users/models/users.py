from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(max_length=500)
    username = models.CharField(max_length=100, blank=True, null=True)  # it's not necessary
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "full_name")

    def __str__(self):
        return f"{self.id}: {self.email}"

