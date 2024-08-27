from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    pass


class biblia(models.Model):
    libro = models.CharField(max_length=22)


class pregunta(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pregunta = models.TextField()
    respuesta = models.TextField()
    libro_id = models.ManyToManyField(biblia,related_name="librito")
    capitulo = models.SmallIntegerField()
    versiculo = models.CharField(max_length=7)


