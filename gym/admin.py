from django.contrib import admin
from .models import User, UserProfile, Post, Room, Message

admin.site.register(UserProfile)
admin.site.register(Post)

admin.site.register(Room)
admin.site.register(Message)
