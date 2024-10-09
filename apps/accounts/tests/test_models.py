import re

import pytest
from django.utils import timezone

from apps.accounts.tests.factory import UserFactory


@pytest.mark.django_db
def test_user_creation():
    user = UserFactory()
    assert user is not None
    assert re.match(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        user.email
    )
    assert user.first_name != ''
    assert user.gender in ['m', 'f']


@pytest.mark.django_db
def test_user_verification_code():
    user = UserFactory()
    verification_code = user.set_email_verification()
    assert user.verification_code == verification_code
    assert 100000 <= verification_code <= 999999


@pytest.mark.django_db
def test_user_verification_status():
    user = UserFactory()

    # Simulating the user verification step
    user.set_is_verified()
    assert user.is_verified
    assert user.date_verified is not None
    assert isinstance(user.date_verified, timezone.datetime)


@pytest.mark.django_db
def test_username_field():
    user = UserFactory()
    assert user.USERNAME_FIELD == 'email'


@pytest.mark.django_db
def test_required_fields():
    user = UserFactory()
    assert 'username' in user.REQUIRED_FIELDS
