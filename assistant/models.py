from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username}: {self.msg}'


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_achieved_score = models.IntegerField(default=0)
    total_possible_score = models.IntegerField(default=0)
    
    