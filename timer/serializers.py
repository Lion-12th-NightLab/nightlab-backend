
from datetime import datetime, timedelta, timezone
from rest_framework import serializers
from .models import Timer

class TimerSerializer(serializers.Serializer):
    start_time = serializers.TimeField(required=False)
    rest_time = serializers.TimeField(required=False)
    stop_time = serializers.TimeField(required=False)

