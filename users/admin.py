from django.contrib import admin
from .models import Messages, Profile, Skill


admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Messages)