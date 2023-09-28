from django.contrib import admin
from .models import User,Posters,Reactions,Follows
# Register your models here.


admin.site.register(Posters)
admin.site.register(Reactions)
admin.site.register(Follows)
