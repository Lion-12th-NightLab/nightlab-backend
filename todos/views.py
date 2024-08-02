
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todos.models import Todo
from todos.serializers import TodoDetailSerializer, TodoCreateSerializer
from users.serializers import UserSerializer

@api_view(['POST', 'GET'])  # POST와 GET 메서드를 처리
@permission_classes([IsAuthenticated])
# todo 생성 및 조회 API
def TodoCreateAndGetAll(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(request.user)
        # Validate the serializer
        if not user_serializer:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = user_serializer.data.get('id')
        todos = request.data.get('todo', [])

        todo_serializer = TodoCreateSerializer(data=todos, many=True)
        if not todo_serializer.is_valid():
            return Response(todo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 요청이 todo list 형태라 반복문으로 저장
        for todo_data in todo_serializer.validated_data:
            text = todo_data.get('text')
            todo = Todo(text=text, user_id=user_id)
            todo.save()  # 각 todo 저장

        return Response({'detail': "성공적으로 생성되었습니다"}, status=status.HTTP_201_CREATED)

    elif request.method == 'GET':
        todos = Todo.objects.filter(user=request.user)  # 해당 사용자의 모든 Todo 항목 조회

        todo_serializer = TodoDetailSerializer(todos, many=True)  # 직렬화

        return Response(todo_serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', 'DELETE'])  # PATCH와 DELETE 메서드를 처리
@permission_classes([IsAuthenticated])
# todo 수정 및 삭제하는 API
def TodoUpdateAndDelete(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)  # 해당 사용자와 일치하는 Todo 조회
    except Todo.DoesNotExist:
        return Response({'detail': 'Todo 항목을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        # RequestBody에서 text를 가져옴
        text = request.data.get('text')
        if text is None:
            return Response({'detail': 'text 필드를 제공해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        todo.text = text  # text 수정
        todo.save()  # 변경 사항 저장
        return Response({'detail': "성공적으로 수정되었습니다"}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        todo.delete()  # Todo 항목 삭제
        return Response({'detail': "성공적으로 삭제되었습니다"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# todo 완료 체크표시 API
def TodoCheckBox(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)  # 해당 사용자와 일치하는 Todo 조회
    except Todo.DoesNotExist:
        return Response({'detail': 'Todo 항목을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    todo.completed = True # 완료 체크
    todo.save()

    return Response({'detail': "성공적으로 수정되었습니다"}, status=status.HTTP_200_OK)


