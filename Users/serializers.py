from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
import random
from .models import User

User = get_user_model()

# USER SERIALIZERS
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_active', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'role': {'default': 'customer'}}

    def create(self, validated_data):
        # Create user instance with inactive status
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'customer'),
            is_active=False  
        )
        user.set_password(validated_data['password'])

        # Generate random 6-digit OTP
        otp_code = f"{random.randint(100000, 999999)}"
        user.verification_code = otp_code
        user.save()

        # Send email with OTP
        send_mail(
            subject="Your Account Verification Code",
            message=f"Hi {user.username},\n\nYour OTP for account verification is: {otp_code}\n\nThank you for registering.",
            from_email="ajaykumaryadav02042000@gmail.com",  # Or use settings.DEFAULT_FROM_EMAIL for dynamic config
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email address.")

        if user.verification_code != otp:
            raise serializers.ValidationError("Invalid OTP.")

        return data

    def save(self, **kwargs):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)
        user.is_active = True
        user.verification_code = None  # clear OTP after verification
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return user


class LogoutSerializer(serializers.Serializer):
    def validate(self, data):
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active']
