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
from .serializers import UserSerializer, UserLogoutSerializer

# from auths.views import login,register,verify
# from users.views import detail, update, logout

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user(request):
    match request.method:
        case 'GET':
            serializer = UserSerializer(request.user)  # instance에 request.user 전달
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'PATCH':
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    serializer = UserSerializer(request.user)
    id = serializer.data.get('id')

    data = MutsaUser.objects.get(id = id)
    data.login = False
    data.save()
    return Response({
        f"logoutId": id,
        "detail": "로그아웃이 완료되었습니다."
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def users_list(request):
    login_user = MutsaUser.objects.filter(login=1)
    serializer = UserSerializer(login_user, many=True)
    return Response(serializer.data)

