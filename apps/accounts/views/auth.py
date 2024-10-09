from django.contrib.auth import authenticate, get_user_model, logout as user_logout
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.accounts.serializers.auth import AccountVerificationSerializer, LoginSerializer, LogoutSerializer, \
    RegisterSerializer, ResendVerificationCodeSerializer, UpdateAccount, UpdatePasswordSerializer, \
    UserWithTokenSerializer
from apps.shared.general_response import GENERAL_SUCCESS_RESPONSE

User = get_user_model()


class UserAuthViewSet(viewsets.GenericViewSet):
    """
    Handles user authentication-related operations.

    This viewset provides user authentication mechanisms

    Methods:
        login(request, *args, **kwargs):
            Authenticates a user and returns a token upon successful login.

        logout(request, *args, **kwargs):
            Blacklist token on logout.

        register(request, *args, **kwargs):
            Register a new user.

        update_account(request, *args, **kwargs):
            Update user's account.

        verify_account(request, *args, **kwargs):
            Verify user's profile using the code sent via WhatsApp.

        resend_verification_code(request, *args, **kwargs):
            Resend verification code

        get_permissions(self):
            Instantiates and returns the list of permissions that this view requires.
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["update_password", "update_account", 'logout']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        Authenticates a user and returns a token upon successful login.
        """
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user is not None:
                return Response(UserWithTokenSerializer(user).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        """
        Blacklist token on logout.
        """
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_logout(request)
            return Response(GENERAL_SUCCESS_RESPONSE, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'])
    def update_password(self, request, pk=None):
        """
        Update user's password.
        """
        user = self.request.user
        serializer = UpdatePasswordSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(GENERAL_SUCCESS_RESPONSE, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """
        Register a new user.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(GENERAL_SUCCESS_RESPONSE, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PUT'], )
    def update_account(self, request):
        """
        Update user's account.
        """
        serializer = UpdateAccount(self.request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def verify_account(self, request):
        """
        Verify user's profile using the code sent via WhatsApp.
        """
        serializer = AccountVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserWithTokenSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def resend_verification_code(self, request):
        """
        Resend verification code
        """
        serializer = ResendVerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(GENERAL_SUCCESS_RESPONSE, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
