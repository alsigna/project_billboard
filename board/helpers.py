from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User

from .models import Author


def get_username(user: User) -> str:
    return Author.objects.get(user=user).user.email


class LocalAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form) -> User:
        user = super().save_user(request, user, form)
        _ = Author.objects.create(user=user)
        return user


class SocialAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None) -> User:
        user = super().save_user(request, sociallogin, form)
        _ = Author.objects.create(user=user)
        return user
