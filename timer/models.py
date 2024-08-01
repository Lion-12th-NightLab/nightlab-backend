from django.db import models
from auths.models import MutsaUser

class Timer(models.Model):
    user = models.ForeignKey(MutsaUser, on_delete = models.CASCADE)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField(null=True, blank=True)
    rest_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        db_table = "timer"
