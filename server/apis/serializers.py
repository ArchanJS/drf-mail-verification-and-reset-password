from rest_framework import serializers
from .models import User
from django.contrib.auth.tokens import default_token_generator

# Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'