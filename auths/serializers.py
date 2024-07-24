from rest_framework import serializers
from .models import MutsaUser

# class UserRegisterRequestSerializer(serializers.Serializer):
#     access_code = serializers.CharField()
#     description = serializers.CharField()

class UserLoginRequestSerializer(serializers.Serializer):
    access_code = serializers.CharField()

class UserTokenReissue(serializers.Serializer):
    refresh_token = serializers.CharField()