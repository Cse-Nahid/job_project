from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import Http404
from rest_framework.generics import RetrieveUpdateAPIView
from jobseeker.permissions import IsJobSeekerOrReadOnly

from .models import JobSeekerProfile
from .serializers import JobSeekerProfileSerializer, JobSeekerRegistrationSerializer
from applications.models import Application
from applications.serializers import ApplicationSerializer

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

User = get_user_model()

class JobSeekerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsJobSeekerOrReadOnly]
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer

class JobSeekerRegistrationAPIView(APIView):
    serializer_class = JobSeekerRegistrationSerializer

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid():
            user = serialized_data.save()

            # creating a token for the user
            token = default_token_generator.make_token(user)

            # creating an unique URL by using the decoded string of the user's unique user ID
            user_id = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f'https://jobhunt-z4ts.onrender.com/jobseeker/active/{user_id}/{token}/'

            # email sending implementation
            email_subject = 'Confirm Your Account'
            email_body = render_to_string('applicant_confirm_email.html', {
                'user': user,
                'confirm_link': confirm_link,
            })

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response({'message': 'Check your mail for confirmation.'}, status=status.HTTP_201_CREATED)

        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

def activate(request, user_id, token):
    try:
        user_id = urlsafe_base64_decode(user_id).decode()
        user = CustomUser._default_manager.get(pk=user_id)
    except(CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('user_login')
    else:
        return redirect('jobseeker_register')

class JobSeekerDataByUserIDView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = JobSeekerProfile.objects.get(user=user_id)
        except JobSeekerProfile.DoesNotExist:
            return Response({'error': 'Jobseeker not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSeekerProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobSeekerProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return JobSeekerProfile.objects.get(user=self.request.user)
        except JobSeekerProfile.DoesNotExist:
            raise Http404

    def get(self, request):
        profile = self.get_object()
        serializer = JobSeekerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        serializer = JobSeekerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobSeekerProfileUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    def get_object(self):
        return JobSeekerProfile.objects.get(user=self.request.user)

# Dashboard and Applications Views
class JobSeekerDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'jobseekerprofile'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        applications = Application.objects.filter(job_seeker=user)
        applications_data = ApplicationSerializer(applications, many=True).data

        return Response({
            'applications': applications_data
        })


class JobSeekerApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        job_seeker = request.user
        applications = Application.objects.filter(job_seeker=job_seeker)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)