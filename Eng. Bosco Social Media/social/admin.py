from django.contrib import admin
from .models import Post, Comment, MaritalStatus, Work,Religion,UserProfile, Notification, ThreadModel, MessageModel
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
class PostAdmin(admin.ModelAdmin):
    inlines=[
        CommentInline,
    ]
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(MaritalStatus)
admin.site.register(Work)
admin.site.register(Religion)
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(ThreadModel)
admin.site.register(MessageModel)

