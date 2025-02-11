import os

import requests
import jwt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer

from rest_framework_simplejwt.tokens import RefreshToken

from auths.models import MutsaUser
from .serializers import MemoRequestSerializer, MemoResponseSerializer

from dotenv import load_dotenv
from .models import Memo
from datetime import timedelta
from django.utils import timezone
from timer.models import Timer
from auths.models import MutsaUser
from datetime import timedelta, datetime, time

load_dotenv()

def get_last_timer(user):
    return Timer.objects.filter(user=user).order_by('-id').first()

def real_time_timer(timer):
    if timer.rest_status:
        return timer.rest_time
    else:
        now_time = timezone.now()
        
        # 한 번도 쉰 적 없고, 종료도 하지 않은 경우
        if timer.rest_date is None and timer.stop_time is None:
            # 현재 시간과 시작 시간 사이의 경과 시간을 계산
            plus_time = now_time - timer.start_date
            
        # 한 번도 쉬지 않은 채로 종료한 경우, 쉬고 종료한 경우
        elif timer.stop_time is not None:
            # 종료 시간과 시작 시간 사이의 경과 시간을 계산
            return timer.stop_time
            
        # 쉬고 다시 시작한 경우
        else:
            plus_time = now_time - timer.rest_date
        
        # Convert timedelta to total seconds
        total_seconds = plus_time.total_seconds()

        # Calculate hours, minutes, and seconds from total seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        try:
            rest_hours = timer.rest_time.hour
            rest_minutes = timer.rest_time.minute
            rest_seconds = timer.rest_time.second
        except AttributeError:
            rest_hours = 0
            rest_minutes = 0
            rest_seconds = 0

        # Add the timedelta to the rest_time
        new_hours = rest_hours + int(hours)
        new_minutes = rest_minutes + int(minutes)
        new_seconds = rest_seconds + int(seconds)
        
        # Handle overflow of seconds and minutes
        if new_seconds >= 60:
            new_seconds -= 60
            new_minutes += 1
        if new_minutes >= 60:
            new_minutes -= 60
            new_hours += 1
        if new_hours >= 24:
            new_hours -= 24  # To stay within the 24-hour range
        
        # Create and return the new time object
        updated_time = time(hour=new_hours, minute=new_minutes, second=new_seconds)
        return updated_time


@swagger_auto_schema(
    method='post',
    operation_id='메모 등록 API',
    operation_description='사용자가 메모를 등록하는 API입니다.',
    tags=['Memo'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='메모 내용'),
        },
        required=['content']  # 필수 필드로 설정
    )
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def memo(request):
    serializer = MemoRequestSerializer(data = request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    user_data = MutsaUser.objects.get(id=user.id)
    user_time = get_last_timer(user)
    if user_time:
        timer = real_time_timer(user_time)
    else:
        timer = time(hour=0, minute=0, second=0)

    content = serializer.validated_data.get('content')

    user_name = user_data.user_name
    profile = user_data.profile
    college = user_data.college

    Memo.objects.filter(user=user).delete()

    memo = Memo.objects.create(
        user=user,
        content=content,  # content를 serializer에서 가져옴
        timer=timer
    )

    response_data = {
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


@swagger_auto_schema(
    method='get',
    operation_id='메모 조회 API',
    operation_description='모든 메모를 조회하는 API입니다.',
    tags=['Memo']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def memo_list(request):
    memos = Memo.objects.all().order_by('-id')

    # Prepare the list of formatted memos
    formatted_memos = []
    for memo in memos:
        user = memo.user
        user_time = get_last_timer(user)
        
        if user_time:
            timer = real_time_timer(user_time)
        else:
            timer = time(hour=0, minute=0, second=0)

        memo.timer = timer
        memo.save()

        formatted_memo = {
            "id": memo.id,
            "content": memo.content,
            "user_name": user.user_name,  # Adjust according to your actual model field names
            "profile": user.profile,  # Adjust according to your actual model field names
            "college": user.college,  # Adjust according to your actual model field names
            "timer": str(timer)  # Assuming timer is a field that you convert to string
        }
        formatted_memos.append(formatted_memo)
    
    response_data = {
        "detail": "memo가 성공적으로 조회되었습니다.",
        "data":
        {
            "memo": formatted_memos
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)

    
    