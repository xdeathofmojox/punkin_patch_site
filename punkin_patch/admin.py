from django.contrib import admin
from .models import Character, PatchTemplate, PatchInstance, Vote

# Register your models here.
admin.site.register(Character)
admin.site.register(PatchTemplate)
admin.site.register(PatchInstance)
admin.site.register(Vote)