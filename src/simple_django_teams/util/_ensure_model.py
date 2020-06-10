from typing import Type

from django.db.models import Model
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


def ensure_model(value, model: Type[Model]):
    """
    Checks that the given value is an instance of a particular model.

    :param value:   The value to check.
    :param model:   The model type to check for.
    """
    if not isinstance(value, model):
        raise TypeError(f"Expected {model.__name__} but got {value.__class__.__name__} instead")


def ensure_user_model(value, allow_anonymous: bool = True):
    """
    Checks that the given value is a user.

    :param value:               The value to check.
    :param allow_anonymous:     Whether to also allow anonymous users.
    """
    if not allow_anonymous or not isinstance(value, AnonymousUser):
        ensure_model(value, get_user_model())
