from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class TypeProgram(models.Model):
    code_program = models.CharField(max_length=2)
    program_name = models.CharField(max_length= 32)

class Students_programs(models.Model):
    userx = models.ManyToManyField(User,related_name="estudiante")
    code = models.ManyToManyField(TypeProgram,related_name="programa")
    status = models.BooleanField(default=False)




