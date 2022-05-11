from rest_framework import serializers
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer

# Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=300)
    class Meta:
        model=User
        fields=['email','password']

class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD