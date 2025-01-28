from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from .models import JobSeekerProfile
from django import forms
from .models import CustomUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = JobSeekerProfile
        fields = '__all__'

class JobSeekerRegistrationSerializer(serializers.ModelSerializer):
    fathers_name = serializers.CharField(max_length=20)
    mothers_name = serializers.CharField(max_length=20)
    address = serializers.CharField()
    contact_no = serializers.CharField(max_length=11, required=False)
    sex = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    age = serializers.IntegerField(validators=[MinValueValidator(18)])
    education = serializers.CharField()
    experience = serializers.CharField()
    confirm_password = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'fathers_name', 'mothers_name',
            'address', 'contact_no', 'sex', 'age', 'education', 'experience',
            'email', 'password', 'confirm_password'
        ]
        user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    def save(self):
        validated_data = self.validated_data
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords do not match."})

        email = validated_data['email']
        if User.objects.filter(email=email, user_type='jobseeker').exists():
            raise serializers.ValidationError({'error': "Email already exists."})

        # Extract user-specific data
        user_data = {k: validated_data.pop(k) for k in ['username', 'first_name', 'last_name']}
        user = User.objects.create(
            **user_data,
            email=email,
            user_type='jobseeker',
            is_active=False  # Initially inactive; activated via email confirmation
        )
        user.set_password(password)
        user.save()

        # Create Jobseeker profile
        JobSeekerProfile.objects.create(user=user, **validated_data)

        return user
