from requests import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from auths.models import MutsaUser
from todos.models import Todo
from todos.serializers import TodoDetailSerializer, TodoCreateSerializer
from users.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTodo(request):

    user_serializer = UserSerializer(request.user)
    # Validate the serializer
    if not user_serializer:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_id = user_serializer.data.get('id')
    user_data = MutsaUser.objects.get(id=user_id)

    todo_serialier = TodoCreateSerializer(data=request.data)

    text = todo_serialier.data.get('text')
    todo = Todo(text=text, user_id=user_id)
    todo.save()

    return Response({'detail' : "성공적으로 생성되었습니다"}, status = status.HTTP_200_OK)

