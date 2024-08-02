from django.db import models
from auths.models import MutsaUser

class Memo (models.Model):
    user = models.ForeignKey(MutsaUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    timer = models.TimeField()

    class Meta:
        db_table = "memo"