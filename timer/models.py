from django.db import models
from auths.models import MutsaUser

class Timer(models.Model):
    user = models.ForeignKey(MutsaUser, on_delete = models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    rest_date = models.DateTimeField(null=True, blank=True)
    stop_date = models.DateTimeField(null=True, blank=True)
    start_time = models.TimeField()
    stop_time = models.TimeField(null=True, blank=True)
    rest_time = models.TimeField(null=True, blank=True)
    rest_status =models.BooleanField(null=True, default=False)

    class Meta:
        db_table = "timer"
