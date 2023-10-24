from django.contrib import admin

# Register your models here.

from .models import ChatRoom, Message, User,UserFollowing 

admin.site.register(User)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(UserFollowing)
