from django.db import models


class ConfirmationCode(models.Model):
    class Actions(models.TextChoices):
        ACCOUNT_CONFIRMATION_BY_EMAIL = ("account_by_email", "Account confirmation code by email")
        PASSWORD_RECOVERY = ("password_recovery", "Password recovery")

    code = models.CharField(max_length=10)
    action = models.CharField(max_length=50, choices=Actions.choices)
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.code}, {self.user}"
