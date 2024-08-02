from rest_framework import serializers
from auths.models import MutsaUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutsaUser
        fields = ['id','nickname']

class UserResponseSerializer(serializers.Serializer):
    college = serializers.CharField()
    user_name = serializers.CharField()
    profile = serializers.CharField()

class UserNicknameSerializer(serializers.Serializer):
    user_name = serializers.CharField()