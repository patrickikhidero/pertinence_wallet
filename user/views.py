from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

from .serializers import CreateUserSerializer, LoginSerializer, LogoutSerializer


class SignupView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer
    


class LogoutView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        refresh_token = RefreshToken(request.data.get('refresh'))
        refresh_token.blacklist()
        return Response("Successful Logout", status=status.HTTP_200_OK)


class LoginView(CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = [IsAuthenticated,]
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        # validation
        if email is None or password is None:
            return Response(errors='Please provide both email and password!', status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        # permission
        if not user:
            return Response(errors={'invalid_credentials': 'Ensure both email and password are correct and you have verify you account'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_verified:
            return Response(errors={'invalid_credentials': 'Please verify your account'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)