# urls.py in accounts app
from django.urls import path
from .views import UserDetailView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
]