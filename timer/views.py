from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from todos.models import Todo
from .serializers import TimerSerializer
from dotenv import load_dotenv
from .models import Timer
from django.utils import timezone

load_dotenv()


@swagger_auto_schema(
    method='post',
    operation_id='타이머 시작 API',
    operation_description='타이머를 시작하는 API입니다.',
    tags=['Timer'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'start_time': openapi.Schema(type=openapi.TYPE_STRING, description='타이머 시작 시간'),
        },
        required=['start_time']  # 필수 필드로 설정
    )
)
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


@swagger_auto_schema(
    method='post',
    operation_id='타이머 정지 API',
    operation_description='타이머를 정지하는 API입니다.',
    tags=['Timer'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'stop_time': openapi.Schema(type=openapi.TYPE_STRING, description='타이머 정지 시간'),
        },
        required=['stop_time']  # 필수 필드로 설정
    )
)
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

        # 현재 사용자의 모든 Todo 항목 조회
        todos = Todo.objects.filter(user = user)

        if todos.exists():
            todos.delete() # 모든 Todo 항목 삭제

        return Response({"detail": "요청이 성공했습니다"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='post',
    operation_id='타이머 휴식 시작 API',
    operation_description='타이머의 휴식을 시작하는 API입니다.',
    tags=['Timer'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'rest_time': openapi.Schema(type=openapi.TYPE_STRING, description='휴식 시작 시간'),
        },
        required=['rest_time']  # 필수 필드로 설정
    )
)
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
    

@swagger_auto_schema(
    method='post',
    operation_id='타이머 휴식 정지 API',
    operation_description='타이머의 휴식을 정지하는 API입니다.',
    tags=['Timer'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={},
        required=[]  # 요청 본체가 필요 없는 경우
    )
)
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