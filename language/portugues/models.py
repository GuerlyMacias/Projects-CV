from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Whyter(models.Model):
    userx= models.ForeignKey(User, on_delete=models.CASCADE, related_name="mywhy")
    why = models.TextField()

    
class Profile(models.Model):
    userx= models.ForeignKey(User, on_delete=models.CASCADE, related_name="profileuser")
    photo = models.ImageField(null=True, blank=True,upload_to="images/")
    country = models.CharField(max_length=20)

class Tester(models.Model):
    userx= models.ForeignKey(User,related_name="testme", on_delete=models.CASCADE)
    number_questions = models.PositiveIntegerField()
    right_answer = models.PositiveIntegerField()



class Lessons(models.Model):
    number_lesson= models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=100)
    theoric = models.TextField()
    urlx = models.URLField()
    videox=models.URLField()
    filex = models.FileField(null=True, blank=True,upload_to="lesspdf/")
class Exams(models.Model):
    lesson = models.ForeignKey(Lessons,on_delete=models.CASCADE, related_name="examlesson")
    question = models.CharField(max_length=255)
    correct = models.CharField(max_length=255)
    false_one = models.CharField(max_length=255)
    false_two = models.CharField(max_length=255)
class Approval(models.Model):
    lessonUser = models.ForeignKey(User, on_delete=models.CASCADE,related_name="aprovaleson")
    number_lesson = models.ManyToManyField(Lessons, blank=True, related_name="aproving")
    bool_lesson_app= models.BooleanField()



class Tips(models.Model):
    tipers = models.TextField()
    created = models.DateTimeField()

class Reactions(models.Model):
    userx = models.ManyToManyField(User,related_name="ReactUser",blank=True)
    tip = models.ManyToManyField(Tips,blank=True,related_name="ReactTip")
    ReactBool = models.BooleanField()



    











