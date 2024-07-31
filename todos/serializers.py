from rest_framework import serializers
from todos.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'user', 'text', 'completed']  # 사용할 필드 설정
        read_only_fields = ['user']  
