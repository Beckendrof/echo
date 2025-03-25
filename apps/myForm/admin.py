from django.contrib import admin
from .models import User, Creator, Editor

# Register your models here.
admin.site.register(User)
admin.site.register(Creator)
admin.site.register(Editor)
