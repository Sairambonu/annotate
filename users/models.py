from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class UserLoginInfo(AbstractBaseUser):
    username = models.CharField(primary_key=True, max_length=50)
    password = models.TextField()
    email = models.CharField(unique=True, max_length=50)
    role = models.CharField(max_length=20, default='annotator')
    phone = models.CharField(max_length=12, default='')
    languages = models.CharField(max_length=100, default='telugu')
    status = models.CharField(max_length=10, default='active')
    last_login = models.DateTimeField(auto_now_add=True)

    # objects = UserLoginInfo()

    is_anonymous = "FALSE"
    is_authenticated = "TRUE"

    is_active = True
    is_superuser = False

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        # managed = False
        db_table = 'user_info'
    
    def __str__(self):
        return self.email