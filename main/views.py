from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from todos.models import Todo
from dotenv import load_dotenv
from timer.models import Timer
from django.utils import timezone
from datetime import timedelta
from auths.models import MutsaUser

@swagger_auto_schema(
    method='get',
    operation_id='전체/실시간 사용 유저 API',
    operation_description='서비스를 이용중인 전체/실시간 사용 유저를 조회하는 API입니다.',
    tags=['Main']
)


@api_view(['GET'])
@permission_classes([AllowAny])
def main(request):
    login_total_user = MutsaUser.objects.all()
    print(login_total_user)
    
    connect_total_user = []
    now_time = timezone.now()

    for user in login_total_user:
        print(user)
        timer = Timer.objects.filter(user=user).order_by('-start_date').first()
        
        if not timer:
            continue

        if timer.start_date is not None and timer.stop_date is None:
            connect_total_user.append(user)
        else:
            connect_time = timer.stop_date + timedelta(minutes=30)
            if connect_time >= now_time:
                connect_total_user.append(user)
            else:
                continue
    
    response_data = {
        "detail": "요청이 성공했습니다.",
        "data": {
            "login_total_user" : len(login_total_user),
            "connect_total_user" : len(connect_total_user),
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)