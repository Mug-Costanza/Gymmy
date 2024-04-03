from django.contrib import admin
from .models import User, UserProfile, Post

admin.site.register(UserProfile)
admin.site.register(Post)

