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
from .serializers import UserLoginRequestSerializer, UserTokenReissue

# from auths.views import login,register,verify
# from users.views import detail, update, logout
from dotenv import load_dotenv

load_dotenv()

def get_jwks_url():
    discovery_url = "https://kauth.kakao.com/.well-known/openid-configuration"
    response = requests.get(discovery_url)
    response.raise_for_status()
    config = response.json()
    return config["jwks_uri"]

def kakao_access_token(access_code):
    response = requests.post(
        'https://kauth.kakao.com/oauth/token',
        headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        },
        data= {
            'grant_type': 'authorization_code',
            'client_id': os.environ.get('KAKAO_REST_API_KEY'),
            'redirect_uri': os.environ.get('KAKAO_REDIRECT_URI'),
            'code': access_code,
        },
    )

    if response.status_code >= 300:
        return Response({'detail': 'Access token 교환에 실패했습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    return response.json()

def kakao_nickname(kakao_data):
    id_token = kakao_data.get('id_token')
    if not id_token:
        return Response({'detail': 'OIDC token 정보를 확인할 수 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        jwks_url = get_jwks_url()
        jwks_client = jwt.PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
        signing_algol = jwt.get_unverified_header(id_token)['alg']
        payload = jwt.decode(
            id_token,
            key=signing_key.key,
            algorithms=[signing_algol],
            audience=os.environ.get('KAKAO_REST_API_KEY'),
        )
        return payload['nickname']
    except (jwt.InvalidTokenError, requests.exceptions.RequestException) as e:
        return Response({'detail': 'OIDC 인증에 실패했습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginRequestSerializer(data = request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    data = serializer.validated_data
    print(data)

    kakao_data = kakao_access_token(data['access_code'])
    print(kakao_data)
    nickname = kakao_nickname(kakao_data)
    print(nickname)

    try:
        user = MutsaUser.objects.get(nickname=nickname)
    except MutsaUser.DoesNotExist:
        user = MutsaUser.objects.create_user(nickname=nickname)
    
    
    refresh = RefreshToken.for_user(user)
    data = MutsaUser.objects.get(nickname=nickname)
    data.login = True
    data.refresh_token = refresh #refresh_token 저장
    data.save()
    
    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    },status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_reissue(request):
    refresh_token_serializer = UserTokenReissue(data=request.data)

    if not refresh_token_serializer.is_valid():
        return Response(refresh_token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    refresh_token = refresh_token_serializer.validated_data['refresh_token']

    try:
        user = MutsaUser.objects.get(refresh_token=refresh_token)
    except MutsaUser.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Refresh token을 사용하여 새로운 access token 생성
        new_access_token = RefreshToken(refresh_token).access_token
    except jwt.InvalidTokenError:
        return Response({'detail': '유효하지 않은 refresh token입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 access token 반환
    return Response({
        'access_token': str(new_access_token)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify(request):
    return Response({'datail': 'Token is verified.'}, status=200)