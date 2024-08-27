from django.contrib import admin
from .models import User,biblia,pregunta
# Register your models here.
admin.site.register(User)
admin.site.register(biblia)
admin.site.register(pregunta)