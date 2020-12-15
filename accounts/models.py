from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class OTP(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    otp = models.IntegerField()