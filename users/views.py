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
from .serializers import UserSerializer

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

@api_view(['GET'])
@permission_classes([AllowAny])
def users_list(request):
    user = MutsaUser.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

