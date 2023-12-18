from django.db import models
from django.contrib.auth.models import User


class Letter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=12)
    message = models.CharField(max_length=100)
    letter_color = models.CharField(max_length=20)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.recipient} - {self.message}'
