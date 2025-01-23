from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('job_seeker', 'Job_seeker'),
        ('viewer', 'Viewer'),
    )
    user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['user_type'] = self.validated_data.get('user_type', '')
        print('heloooooooo --- > ',data['user_type'])
        return data

    def save(self, request):
        user = super().save(request)
        user.user_type = self.cleaned_data.get('user_type')
        user.save()
        return user

# creating login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True, max_length=20)

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type']
