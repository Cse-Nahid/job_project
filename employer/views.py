from django.shortcuts import render, redirect
from rest_framework import viewsets, status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from employer.permissions import IsEmployerOrReadOnly, IsEmployerUser

from .models import EmployerProfile
from .serializers import EmployerProfileSerializer, EmployerRegistrationSerializer


# necessary importing for confirmation link generating
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes

# to implement email sending functionality
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


from accounts.models import CustomUser


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

# Importing models
from employer.models import EmployerProfile  # Assuming this model exists in the employer app
from jobs.models import Job  # Assuming the job model is defined here
from applications.models import Application  # Assuming the application model is defined here

# Importing serializers
from employer.serializers import EmployerProfileSerializer  # Assuming this serializer exists
from jobs.serializers import JobSerializer  # Assuming this serializer exists
from applications.serializers import ApplicationSerializer  # Assuming this serializer exists





User = get_user_model()




# Create your views here.
class EmployerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployerOrReadOnly]

    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer




# Creating user registration functionality
class EmployerRegistrationAPIView(APIView):
    serializer_class = EmployerRegistrationSerializer

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid():
            user = serialized_data.save()

            # Generate token and user ID
            token = default_token_generator.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.pk))

            # Create confirmation link
            confirm_link = f'https://job-project-delta.vercel.app/employer/active/{user_id}/{token}/'

            # Prepare and send email
            email_subject = 'Confirm Your Account'
            email_body = render_to_string('employer_confirm_email.html', {
                'user': user,
                'confirm_link': confirm_link,
            })

            try:
                email = EmailMultiAlternatives(email_subject, '', to=[user.email])
                email.attach_alternative(email_body, 'text/html')
                email.send()
            except Exception as e:
                return Response({'error': 'Email sending failed.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Check your mail for confirmation.'}, status=status.HTTP_201_CREATED)

        # Handle validation errors
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)






# creating a function to decode the confirmation link for activating the user account
def activate(request, user_id, token):
    try:
        user_id = urlsafe_base64_decode(user_id).decode()
        user = CustomUser._default_manager.get(pk = user_id)
    except(CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('user_login')
        return redirect('https://cse-nahid.github.io/jobs_fronted/employer/login.html')
    else:
        # er age response ba kono error message die deowa jete pare
        return redirect('employer_register')







# to get the specific job_seeker object data by an user_id
class EmployerDataByUserIDView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = EmployerProfile.objects.get(user=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = EmployerProfileSerializer(user)
        print('user:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


# profile

    class EmployerProfileListCreateView(APIView):
        def get(self, request):
            profiles = EmployerProfile.objects.all()
            serializer = EmployerProfileSerializer(profiles, many=True)
            return Response(serializer.data)

    def post(self, request):
        # Check if a profile already exists for the user
        user_id = request.data.get("user")
        if EmployerProfile.objects.filter(user_id=user_id).exists():
            return Response(
                {"error": "A profile already exists for this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = EmployerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerProfileDetailView(APIView):

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def get(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = self.get_object()
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployerProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer


class EmployerProfileUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployerProfileSerializer

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def put(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Dashboard and Applications Views
class EmployerDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'employerprofile'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        jobs = Job.objects.filter(employer=user)
        jobs_data = JobSerializer(jobs, many=True).data

        applications = Application.objects.filter(job__in=jobs)
        applications_data = ApplicationSerializer(applications, many=True).data

        return Response({
            'jobs': jobs_data,
            'applications': applications_data
        })


class EmployerApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_id = request.user.id
        jobs = Job.objects.filter(employer_id=employer_id)
        applications = Application.objects.filter(job__in=jobs)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
