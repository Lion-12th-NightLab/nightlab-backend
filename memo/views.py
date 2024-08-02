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
from .serializers import MemoRequestSerializer, MemoResponseSerializer

from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from dotenv import load_dotenv
from .models import Memo
from datetime import timedelta
from django.utils import timezone
from timer.models import Timer
from auths.models import MutsaUser

load_dotenv()

def get_last_timer(user):
    return Timer.objects.filter(user=user).order_by('-id').first()

def real_time_timer(timer):
    if timer.rest_status == True:
        return timer.rest_time
    else:
        print("time 시작")
        now_time = timezone.now()
        plus_time = now_time - timer.rest_date
        print(plus_time)
        print(timer.rest_time)
        time = timer.rest_time +  plus_time
        return time


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def memo(request):
    serializer = MemoRequestSerializer(data = request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    user_data = MutsaUser.objects.get(id=user.id)
    time = get_last_timer(user)
    timer = real_time_timer(time)
    content = serializer.validated_data.get('content')

    user_name = user_data.user_name
    profile = user_data.profile
    college = user_data.college

    memo = Memo.objects.create(
        user=user,
        content=content,  # content를 serializer에서 가져옴
        timer=timer
    )

    response_data = {
        "code": 200,
        "detail": "memo가 성공적으로 등록되었습니다.",
        "data": {
            "id": memo.id,
            "content": memo.content,
            "user_name": user_name,
            "profile": profile,
            "college": college,
            "timer": str(timer)  # timer를 문자열로 변환
        }
    }

    return Response(response_data, status=status.HTTP_201_CREATED)




    
    