import json
from io import BytesIO

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.accounts.tests.factory import UserFactory
from apps.shared.general_response import GENERAL_SUCCESS_RESPONSE


@pytest.mark.django_db
class TestUserAuthViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_verify_account_success(self):
        # Generate a user and set the verification code
        user = self.user
        user.set_email_verification()

        # Prepare payload and URL
        payload = {
            'email': user.email, 'verification_code': user.verification_code,
            'password': 'thepassword123'
        }
        url = reverse('auth-verify-account')

        # Make the API request
        response = self.client.post(url, data=json.dumps(payload), content_type='application/json')

        # Validate the response
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data
        assert User.objects.get(email=user.email).is_verified is True

    def test_verify_account_fail(self):
        # Generate a user and set the verification code
        self.user.is_verified = False
        self.user.save()

        # Prepare payload and URL with wrong verification_code
        payload = {'email': self.user.email, 'verification_code': 'wrong_code'}
        url = reverse('auth-verify-account')

        # Make the API request
        response = self.client.post(url, data=json.dumps(payload), content_type='application/json')

        # Validate the response
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resend_verification(self):
        url = reverse('auth-resend-verification-code')
        payload = {'email': self.user.email}

        # Test when user is not verified
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_invalid_email(self):
        # Test when whatsapp number is invalid
        url = reverse('auth-resend-verification-code')
        self.user.set_is_verified()
        payload = {'email': 'invalid_email'}
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.json()

    def test_login(self):
        url = reverse('auth-login')
        payload = {'email': self.user.email, 'password': 'password'}

        # Test successful login
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.json()

        # Test unsuccessful login with wrong password
        payload['password'] = 'wrong_password'
        response = self.client.post(url, json.dumps(payload), content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'non_field_errors' in response.json()

    def test_update_account_success(self):
        # Create a user using factory_boy
        user = self.user

        # Update profile data payload
        payload = {'first_name': 'Updated', 'last_name': 'Name'}

        # Making the API call
        url = reverse('auth-update-account')
        response = self.client.put(url, json.dumps(payload), content_type='application/json')

        # Refresh user instance from DB
        user.refresh_from_db()

        # Assertions
        assert response.status_code == 200
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'

    def test_update_account_unauthenticated(self):
        # Update profile data payload
        payload = {'first_name': 'Updated', 'last_name': 'Name'}
        self.client.credentials()
        # Making the API call
        url = reverse('auth-update-account')
        response = self.client.put(url, json.dumps(payload), content_type='application/json')

        # Assertions
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile_with_photo(self):
        user = self.user
        # Create an image using PIL
        image = Image.new('RGB', (100, 100), color=(73, 109, 137))
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')

        # Create SimpleUploadedFile for avatar
        avatar = SimpleUploadedFile('avatar.jpg', img_byte_arr.getvalue(), content_type='image/jpeg')

        # Update profile data payload
        payload = {'first_name': 'Updated', 'last_name': 'Name', 'avatar': avatar, }

        # Making the API call
        url = reverse('auth-update-account')
        response = self.client.put(url, payload, format='multipart')

        # Refresh user instance from DB
        user.refresh_from_db()

        # Assertions
        assert response.status_code == 200
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'
        assert user.avatar is not None

    def test_logout_success(self):
        # Define the request data, in this case, provide a valid refresh token
        data = {'refresh_token': str(RefreshToken.for_user(self.user))}
        url = reverse('auth-logout')

        # Make a POST request to the logout endpoint
        response = self.client.post(url, data, format='json')

        # Assert that the response content matches the expected success response
        assert response.json() == GENERAL_SUCCESS_RESPONSE
        # Assert that the response status code is HTTP 200 OK
        assert response.status_code == status.HTTP_200_OK

    def test_logout_invalid_token(self):
        # Define the request data with an invalid refresh token
        data = {'refresh_token': 'invalid_refresh_token'}
        url = reverse('auth-logout')

        # Make a POST request to the logout endpoint
        response = self.client.post(url, data, format='json')

        # Assert that the response status code is HTTP 400 Bad Request
        assert response.status_code == status.HTTP_400_BAD_REQUEST
