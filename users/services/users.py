import random

from users.models import User, ConfirmationCode


def create_verification_account_code(user: User) -> ConfirmationCode:
    code = str(random.randint(1000, 9999))
    return ConfirmationCode.objects.create(
        code=code, action=ConfirmationCode.Actions.ACCOUNT_CONFIRMATION_BY_EMAIL, user=user
    )


def send_email_verification_code(to: User, code: ConfirmationCode):
    print(f"-- send email to: {to} code {code}")


def change_user_password(user: User, new_password: str):
    user.set_password(new_password)
    user.save()