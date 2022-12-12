from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    expiration_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
