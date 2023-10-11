from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'message': 'User registered successfully.', 'username': user.username, 'access_token': access_token})
            
            return Response({'message': 'Something went wrong!'})
        except Exception as e:
            print(e)
            Response({ 'Error': e })

class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            user = User.objects.filter(username=username).first()
            if user is None or not user.check_password(password):
                return Response({'error': 'Invalid credentials'})
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'message': 'User logged in successfully.', 'access_token': access_token})
        except Exception as e:
            print(e)
            Response({ 'Error': e })

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)