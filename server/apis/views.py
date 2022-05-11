from functools import partial
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import io
from rest_framework.parsers import JSONParser
from .models import User
from .serializers import UserSerializer,UserLoginSerializer,TokenObtainPairSerializer
from .utils import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CreateUser(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def perform_create(self, serializer):
        obj=serializer.save()
        verifyEmail(obj.email,obj.uid)

# Verify user
@api_view(['PATCH'])
def verifyUser(request):
    try:
        io_data=io.BytesIO(request.body)
        py_data=JSONParser().parse(io_data)
        user=User.objects.get(email=py_data['email'])
        if User.objects.filter(email=py_data['email']).exists() and py_data['key']==user.uid:
            serialized_user=UserSerializer(user,data={'verified':True},partial=True)
            if serialized_user.is_valid():
                serialized_user.save()
        else:
            raise ValueError("Key didn't match didn't match!")

        return JsonResponse({'message':'User verified'},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'Something went wrong!'},status=status.HTTP_400_BAD_REQUEST)

# User login
class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data['email']
            password=serializer.data['password']
            user=User.objects.get(email=request.data['email'])
            token=Token.objects.get_or_create(user=user)

# Generate token
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

# Update user
class GetOrUpdateUser(generics.RetrieveUpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]