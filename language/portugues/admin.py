from django.contrib import admin
from .models import User,Profile,Approval,Tester,Lessons,Exams,Whyter,Reactions
# Register your models here.

admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Approval)
admin.site.register(Tester)
admin.site.register(Lessons)
admin.site.register(Exams)
admin.site.register(Whyter)
admin.site.register(Reactions)
