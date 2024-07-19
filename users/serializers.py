from rest_framework import serializers
from auths.models import MutsaUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutsaUser
        fields = ['id','nickname','description','age','mbti']

class UserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutsaUser
        fields = '__all_'