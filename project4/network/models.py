from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posters(models.Model):
    userx= models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    poster = models.CharField(max_length=600)
    created = models.DateTimeField()
    EditBool = models.BooleanField()
    edited = models.DateTimeField()

class Reactions(models.Model): 
    post_number=models.ManyToManyField(Posters,related_name="reaction")
    likes = models.BigIntegerField()
    userx = models.ForeignKey(User, blank=True,on_delete=models.CASCADE)

class Follows(models.Model):
    userx = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="userFollowed")
    followers = models.ManyToManyField(User, related_name="followers")
    FollowBool = models.BooleanField()
    quantityF = models.BigIntegerField()

