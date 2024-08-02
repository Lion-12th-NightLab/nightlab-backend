from rest_framework import serializers
from .models import Memo

class MemoRequestSerializer(serializers.Serializer):
    content = serializers.CharField()

class MemoResponseSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    user_name = serializers.CharField()
    profile = serializers.CharField()
    college = serializers.CharField()
    timer = serializers.TimeField()

    class Meta:
        model = Memo
        fields = ['id','content', 'user_name', 'profile', 'college', 'timer']