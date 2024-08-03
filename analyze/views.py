import os

import requests
import jwt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework_simplejwt.tokens import RefreshToken

from auths.models import MutsaUser

from dotenv import load_dotenv
from datetime import timedelta
from django.utils import timezone
from timer.models import Timer
from auths.models import MutsaUser
from datetime import timedelta, time
from django.db.models import Avg, Q

def calculate_average_time(timers):
    total_seconds = 0
    for timer in timers:
        total_seconds += timer.stop_time.hour * 3600 + timer.stop_time.minute * 60 + timer.stop_time.second

    if timers:
        average_seconds = total_seconds / len(timers)
        hours, remainder = divmod(average_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        average_time = time(hour=int(hours), minute=int(minutes), second=int(seconds))
        return average_time
    else:
        return time(hour=0, minute=0, second=0)
    
def round(time1, time2):
    hour = time1.hour - time2.hour
    minute = time1.minute - time2.minute
    if minute >= 30:
        hour += hour
    return hour


@swagger_auto_schema(
    method='get',
    operation_id='분석 리포트 조회 API',
    operation_description='사용자의 일주일간 야간작업 분석 리포트를 조회하는 API입니다.',
    tags=['Analyze']
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analyze(request):
    user = MutsaUser.objects.get(id = request.user.id)
    
    # 현재 날짜와 일주일 전 날짜 계산
    now = timezone.now()
    one_week_ago = now - timedelta(weeks=1)
    
    # 일주일 이내의 stop_date를 가진 타이머 필터링
    all_timers = Timer.objects.filter(stop_time__isnull=False, stop_date__gte=one_week_ago)
    same_college_users = MutsaUser.objects.filter(college=user.college)
    college_timers = Timer.objects.filter(user__in=same_college_users, stop_time__isnull=False, stop_date__gte=one_week_ago)
    user_timers = Timer.objects.filter(user=user, stop_time__isnull=False, stop_date__gte=one_week_ago)
    
    # 평균 시간 계산
    total_average_time = calculate_average_time(all_timers)
    college_average_time = calculate_average_time(college_timers)
    user_average_time = calculate_average_time(user_timers)


    response_data = {
        "detail": "요청이 성공했습니다.",
        "data": {
            "user_name": user.user_name,
            "college": user.college,
            "profile": user.profile,
            "college_average" : college_average_time, #단과대학 평균 야작시간
            "total_average" : total_average_time, # 전체유저 평균 야작시간
            "user_average" : user_average_time, # 해당 유저 하루 평균 야작시간
            "college_comparison" : round(college_average_time,user_average_time), # 되도록 정수타입으로 보내주기
            "total_comparison" : round(total_average_time,user_average_time)# 되도록 정수타입으로 보내주기
        }
    }

    return Response(response_data, status=status.HTTP_201_CREATED)