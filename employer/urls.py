from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
# from employer.permissions import IsEmployerOrReadOnly, IsEmployerUser


# Create a router
router = DefaultRouter()

# register ViewSets with the router.

# Register the EmployerViewSet
router.register('list', EmployerViewSet, basename='employer')

# Register the EmployerProfileViewSet
router.register('profiles', EmployerProfileViewSet, basename='employer-profile')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),

    path('register/', EmployerRegistrationAPIView.as_view(), name='employer_register'),
    path('active/<user_id>/<token>/', activate, name='employer_account_activate'),

    path('by_user_id/', EmployerDataByUserIDView.as_view(), name='employer_by_user_id'),

    path('dashboard/', EmployerDashboardView.as_view(), name='employer-dashboard'),
     path('applications/', EmployerApplicationsView.as_view(), name='employer-applications'),
    path('profile/', EmployerProfileDetailView.as_view(), name='employer-profile-detail'),
    path('profile/edit/', EmployerProfileUpdateView.as_view(), name='employer-profile-update'),
]