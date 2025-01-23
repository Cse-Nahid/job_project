from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
 # Add this import at the top of your file



# Create a router
router = DefaultRouter()

# register ViewSets with the router.
router.register('list', JobSeekerViewSet)



# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),

    path('register/', JobSeekerRegistrationAPIView.as_view(), name='jobseeker_register'),

    path('active/<user_id>/<token>/', activate, name='jobseeker_account_activate'),
    
    path('by_user_id/', JobSeekerDataByUserIDView.as_view(), name='jobseeker_by_user_id'),


    path('dashboard/', JobSeekerDashboardView.as_view(), name='jobseeker-dashboard'),
    path('applications/', JobSeekerApplicationsView.as_view(), name='jobseeker-applications'),
    path('profile/', JobSeekerProfileDetailView.as_view(), name='jobseeker-profile-detail'),
    path('profile/edit/', JobSeekerProfileUpdateView.as_view(), name='jobseeker-profile-update'),
]