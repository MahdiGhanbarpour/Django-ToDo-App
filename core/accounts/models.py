from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserManager(BaseUserManager):
    '''
    A custom User Manager
    '''
    def create_user(self, username, password, **kwargs) :
        '''
        A function to create user with given username and password
        '''
        if not username:
            raise ValueError(_("Name must be set"))
        
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, username, password, **kwargs):
        """
        A function to create super user with given username and password
        """
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)
        
        if kwargs.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    '''
    A custom user model
    '''
    username = models.CharField(max_length=250, unique=True)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self) :
        return self.username