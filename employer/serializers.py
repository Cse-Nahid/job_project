from rest_framework import serializers
from django.contrib.auth import authenticate
from django import forms
from .models import EmployerProfile, CustomUser
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()


class EmployerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = EmployerProfile
        fields = "__all__"


class EmployerRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password", "first_name", "last_name"]

    # Add user_type as a serializer field, if applicable
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=False)

    def validate(self, data):
        """
        Ensure passwords match and perform any additional validation here.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        return data

    def create(self, validated_data):
        """
        Create a new user and associated employer profile.
        """
        # Remove `confirm_password` as it's not part of the user model
        validated_data.pop("confirm_password")

        # Create the user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        # Add additional fields to EmployerProfile
        EmployerProfile.objects.create(
            user=user,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            user_type=validated_data.get("user_type", None)
        )

        return user


class EmployerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """
        Authenticate user credentials.
        """
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "This account is inactive."})

        return data
