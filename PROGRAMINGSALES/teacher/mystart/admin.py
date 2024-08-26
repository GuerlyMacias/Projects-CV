from django.contrib import admin
from .models import User,Students_programs,TypeProgram

# Register your models here.

admin.site.register(User)
admin.site.register(Students_programs)
admin.site.register(TypeProgram)