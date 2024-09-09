from django.db import models
from django.contrib.auth import get_user_model

# Getting user model object
user = get_user_model()

# Create your models here.
class Task(models.Model):
    '''
    Tasks model
    '''
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    
    is_done = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.title