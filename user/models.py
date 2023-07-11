from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

# extending default user class
class User(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictur", blank=True, null=True)



class address(models.Model):

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)


