# views.py in accounts app
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

from .serializers import LoginSerializer, UserAccountSerializer

from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


User = get_user_model()




# to get the user object data by an user_id
class UserDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = UserAccountSerializer(user)
        print('user:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)





# creating views for login functionality
# class LoginAPIView(APIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serialized_data = self.serializer_class(data = request.data)

#         if serialized_data.is_valid():
#             username = serialized_data.validated_data['username']
#             password = serialized_data.validated_data['password']
#             user = authenticate(username = username, password = password)

#             if user:
#                 # The method get_or_create returns a tuple containing two elements
#                 token, _ = Token.objects.get_or_create(user = user)
#                 print(token)    # getting token
#                 print(_)    # indicates whether the token_object was created or not
#                 login(request, user)
#                 return Response({'token': token.key, 'user_id': user.id})
#             else:
#                 return Response({'error': 'Invalid credential'})
        
#         return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Check if the account is active
            if user.is_active:
                # Generate or get the token for the user
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "This account is disabled."}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Return error message for invalid credentials
            return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


# creating views for logout functionality
# class LogoutAPIView(APIView):
#     def get(self, request):
#         logout(request)
#         # return redirect('user_login')
#         return Response('Logout successful.')


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"success": True, "message": "Logout successful."}, status=status.HTTP_200_OK)