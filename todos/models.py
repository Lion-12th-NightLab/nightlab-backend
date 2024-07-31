from django.db import models
from auths.models import MutsaUser

class Todo(models.Model):
    user = models.ForeignKey(MutsaUser, on_delete=models.CASCADE, related_name='todos')  
    text = models.CharField(max_length=256)  # todo의 내용
    completed = models.BooleanField(default=False)  # 완료 여부

    class Meta:
        db_table = 'todo'  # 테이블 이름

   