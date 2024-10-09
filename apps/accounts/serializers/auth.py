from django.contrib.auth import authenticate, get_user_model, password_validation
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.general_response import INVALID_LOGIN
from apps.shared.literals import ACCESS_TOKEN, EMAIL, NEW_PASSWORD, OLD_PASSWORD, REFRESH_TOKEN, VERIFICATION_CODE
from apps.shared.utils.helpers import generate_tokens

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user is None:
            raise serializers.ValidationError(INVALID_LOGIN)
        attrs['user'] = user
        return attrs


class UserWithTokenSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'groups', 'access_token', 'refresh_token'
        ]

    def to_representation(self, user):
        ret = super().to_representation(user)

        tokens = generate_tokens(user)

        ret[ACCESS_TOKEN] = tokens['access_token']
        ret[REFRESH_TOKEN] = tokens['refresh_token']

        return ret


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def create(self, validated_data):
        token = RefreshToken(validated_data[REFRESH_TOKEN])
        token.blacklist()
        return token

    def validate_refresh_token(self, val):
        try:
            RefreshToken(val)
        except TokenError:
            raise serializers.ValidationError('Refresh token is blacklisted and cannot be used. '
                                              'Try login instead to get a new refresh token')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        validators=[password_validation.validate_password],
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'email', 'password'
        ]

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        code = user.set_email_verification()
        # TODO: Add user to group
        # TODO: Send verification code
        user.save()
        return user


class AccountVerificationSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField()
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        verification_code = validated_data[VERIFICATION_CODE]
        email = validated_data[EMAIL]

        try:
            user = User.objects.get(email=email, verification_code=verification_code)
            user.set_is_verified()
            user.save()

        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Email or Verification code')

        return user


class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        email = validated_data[EMAIL]

        try:
            user = User.objects.get(email=email)
            user.set_email_verification()
            # TODO: Send verification code
            user.save()

        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Email')

        return user


class UpdateAccount(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'first_name', 'last_name', 'phone_number'
        ]


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.instance
        if user.check_password(attrs.get(OLD_PASSWORD)):
            return attrs
        raise serializers.ValidationError("The old password is invalid")

    def update(self, instance, validated_data):
        instance.set_password(validated_data[NEW_PASSWORD])
        instance.save()
        return instance
