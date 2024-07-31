
from datetime import datetime, timedelta, timezone
from rest_framework import serializers
from .models import Timer

class TimerSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField(required=False)
    rest_time = serializers.DateTimeField(required=False)
    stop_time = serializers.DateTimeField(required=False)

