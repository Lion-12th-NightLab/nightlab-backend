import os

import requests
import jwt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer

from rest_framework_simplejwt.tokens import RefreshToken

from auths.models import MutsaUser
from .serializers import TimerSerializer

from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from dotenv import load_dotenv
from .models import Timer
from datetime import timedelta
from django.utils import timezone

load_dotenv()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def timer_start(request):
    serializer = TimerSerializer(data = request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 사용자 정보 추가
    validated_data = serializer.validated_data
    user = request.user
    
    # 타이머 객체 생성
    timer = Timer.objects.create(
        user=user,
        start_time=validated_data.get('start_time'),
        start_date=timezone.now() 
    )
    return Response({"detail": "요청이 성공했습니다."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def timer_stop(request):
    serializer = TimerSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user = request.user

    # 최근에 시작된 타이머를 찾습니다.
    try:
        recent_timer = Timer.objects.filter(user=user).order_by('-start_date').first()

        if not recent_timer:
            return Response({"detail": "시작된 타이머가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        recent_timer.stop_time = validated_data.get('stop_time')
        recent_timer.stop_date = timezone.now() 
        recent_timer.save()

        return Response({"detail": "요청이 성공했습니다"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def timer_rest_start(request):
    serializer = TimerSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user = request.user

    try:
        recent_timer = Timer.objects.filter(user=user).order_by('-start_date').first()

        if not recent_timer:
            return Response({"detail": "시작된 타이머가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        recent_timer.rest_time = validated_data.get('rest_time')
        recent_timer.rest_status = True
        recent_timer.save()
        return Response({"detail": "요청이 성공했습니다"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": f"서버에서 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def timer_rest_stop(request):
    serializer = TimerSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    user = request.user

    try:
        recent_timer = Timer.objects.filter(user=user).order_by('-start_date').first()

        if not recent_timer:
            return Response({"detail": "시작된 타이머가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        recent_timer.rest_date = timezone.now()
        recent_timer.rest_status = False
        recent_timer.save()

        recent_timer.save()
        return Response({"detail": "요청이 성공했습니다"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": f"서버에서 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)