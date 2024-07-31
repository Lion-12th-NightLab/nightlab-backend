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
from .serializers import UserSerializer, UserResponseSerializer, UserNicknameSerializer

# from auths.views import login,register,verify
# from users.views import detail, update, logout

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

@api_view(['GET'])
@permission_classes([AllowAny])
def users_list(request):
    user = MutsaUser.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

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

