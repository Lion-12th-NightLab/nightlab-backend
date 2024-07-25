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
from .serializers import UserEmailSerializer, UserSerializer, UserVerifycodeSerializer

from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from .models import Verify

# from auths.views import login,register,verify
# from users.views import detail, update, logout
from dotenv import load_dotenv

load_dotenv()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendVerification(request):
    email_serializer = UserEmailSerializer(data=request.data)
    print(email_serializer)
    if not email_serializer.is_valid():
        return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = email_serializer.validated_data.get('email')
    print(email)
    
    # Serialize the user data
    user_serializer = UserSerializer(request.user)

    # Validate the serializer
    if not user_serializer:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = user_serializer.data.get('id')
    user_data = MutsaUser.objects.get(id=user_id)

    if not email:
        return Response({"message": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
    if MutsaUser.objects.filter(email=email).exists():
        return Response({"message": "이미 사용 중인 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
    # 이미 인증코드가 존재할 경우
    if Verify.objects.filter(user=user_data).exists(): 
        Verify.objects.filter(user=user_data).delete()
        
    # 새로운 인증 코드 생성
    verification_code = get_random_string(length=6)
    message = f"인증코드는 {verification_code}입니다."
    print(message)
    # 이메일 발송
    email_message = EmailMessage(
        subject='Verification Code',
        body=message,
        to=[email],
    )
    email_message.send()
        
    
    # 데이터베이스에 인증 코드 저장
    
    user_data.email = email
    verify_code = Verify(user=user_data, verify_code =verification_code)
    user_data.save()
    verify_code.save()
        
    return Response({'message': '인증 코드가 이메일로 발송되었습니다.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CheckVerifycode(request):
    serializer = UserVerifycodeSerializer(data=request.data)
    # Validate the serializer
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = request.user
    user_data = MutsaUser.objects.get(id=user.id)

    try:
        verify_instance = Verify.objects.get(user=user_data)
    except Verify.DoesNotExist:
        verify_instance = None
        return Response({"message": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    if verify_instance.verify_code == serializer.validated_data.get('verify_code'):
        return Response({"message": "인증되었습니다."}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "인증을 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST)


