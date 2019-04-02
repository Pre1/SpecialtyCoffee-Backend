from django.db import models


class Status(models.Model):
    title = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
