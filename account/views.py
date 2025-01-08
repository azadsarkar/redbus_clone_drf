from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, MyTokenObtainPairSerializer, UserUpdateDeleteserializer, UserChangePassword
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import Token

# Create your views here.

class UserRegistrationAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]



class MyObtainTokenPairView(TokenObtainPairView):

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserUpdateDeleteserializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    

class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = UserChangePassword
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(status=status.HTTP_200_OK)
    