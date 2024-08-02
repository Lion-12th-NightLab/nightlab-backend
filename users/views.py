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
from .serializers import UserSerializer, UserResponseSerializer, UserNicknameSerializer

# from auths.views import login,register,verify
# from users.views import detail, update, logout

@swagger_auto_schema(
    method='post',
    operation_id='사용자 추가 정보 등록 API',
    operation_description='로그인 시 사용자의 추가 정보를 등록하는 API입니다.',
    tags=['Auth'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'college': openapi.Schema(type=openapi.TYPE_STRING, description='사용자의 단과 대학'),
            'user_name': openapi.Schema(type=openapi.TYPE_STRING, description='사용자의 닉네임'),
            'profile': openapi.Schema(type=openapi.TYPE_STRING, description='사용자의 프로필 정보'),
        },
        required=['college', 'user_name', 'profile']  # 필수 필드로 설정
    )
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_signup(request):
    match request.method:
        case 'POST':
            serializer = UserResponseSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            user.college = serializer.validated_data.get('college')
            user.user_name = serializer.validated_data.get('user_name')
            user.profile = serializer.validated_data.get('profile')      
            
            user.save()
            return Response({"detail": "가입에 성공하였습니다."},status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='사용자 목록 조회 API',
    operation_description='모든 사용자의 목록을 조회하는 API입니다.',
    tags=['User'],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def users_list(request):
    user = MutsaUser.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_id='닉네임 중복 체크 API',
    operation_description='사용자가 입력한 닉네임의 중복 여부를 확인하는 API입니다.',
    tags=['Auth'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_name': openapi.Schema(type=openapi.TYPE_STRING, description='확인할 닉네임'),
        },
        required=['user_name']  # 필수 필드로 설정
    )
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def nickname_check(request):
    serializer = UserNicknameSerializer(data=request.data)
    if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    request_nickname = serializer.validated_data.get('user_name')

    # 닉네임 중복 체크
    if MutsaUser.objects.filter(user_name=request_nickname).exists():
        return Response({"detail": "중복된 닉네임입니다."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "사용 가능한 닉네임입니다."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='회원정보 조회 API',
    operation_description='마이페이지에서 사용자의 정보를 조회하는 API입니다.',
    tags=['User']
)
@swagger_auto_schema(
    method='patch',
    operation_id='회원정보 수정 API',
    operation_description='마이페이지에서 사용자의 정보를 수정하는 API입니다.',
    tags=['User'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'profile': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 프로필'),
            'user_name': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 이름'),
            'college': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 대학'),
        },
        required=[]  # 특정 필드를 필수로 하지 않을 경우 빈 배열로 설정
    )
)
@api_view(['GET','PATCH'])  # POST와 GET 메서드를 처리
@permission_classes([IsAuthenticated])
# 회원정보 조회 및 수정
def MypageGetAndUpdate(request):
    if request.method == 'GET':
        # 현재 인증된 사용자 가져오기
        user = request.user
        # 사용자 정보 조회
        user_data = {
            'profile': user.profile,
            'user_name': user.user_name,
            'college': user.college,
        }
        # 직렬화
        user_serializer = UserResponseSerializer(data=user_data)
        if user_serializer.is_valid():
            return Response(user_serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=400)



