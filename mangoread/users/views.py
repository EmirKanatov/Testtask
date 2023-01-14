from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile

from .serializer import RegisterSerializer, LoginSerializer, RestorePasswordSerializer, ChangePasswordSerializer, \
    UserSerializer, ProfileSerializer


# Create your views here.

class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={'message': 'ok'})
        else:
            return Response(data={'message': 'Registration failed'})


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        serializer = LoginSerializer(data=self.request.data,
                                                 context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(data={'user': user})


class RestorePasswordAPIView(generics.GenericAPIView):
    serializer_class = RestorePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get("new_password") == serializer.validated_data.get("confirm_password"):
                if len(serializer.validated_data.get("confirm_password")) >= 8:
                    user = request.user
                    user.set_password(serializer.validated_data.get("confirm_password"))
                    user.save()
                    return Response({'message': 'Password updated successfully'})
                else:
                    return Response({'message': 'Password is too short'})
            else:
                return Response({'message': "Passwords don't match"})
        return Response({'message': "Password can't be blank"})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Password successfully updated')


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
