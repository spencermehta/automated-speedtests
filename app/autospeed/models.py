from django.db import models
from django.shortcuts import reverse


class SpeedtestResult(models.Model):
    datetime = models.DateTimeField()
    download = models.FloatField()
    upload = models.FloatField()
    ping = models.FloatField()

    def __str__(self):
        return ("%s, %s, %s, %s", self.datetime, self.download, self.upload, self.ping)
