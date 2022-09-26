from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):
    body=models.TextField()
    created_on=models.DateTimeField(default=timezone.now)
    date_time=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    post_image=models.ImageField(blank=True, null=True, upload_to='post/post_pictures/')
    # image=models.ManyToManyField('Image', blank=True, null=True)
    likes=models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes=models.ManyToManyField(User, blank=True, related_name='dislikes')
    
    #tags = models.ManyToManyField('Tag', blank=True)

    shared_body=models.TextField(blank=True, null=True)
    shared_on=models.DateTimeField(blank=True, null=True)
    shared_user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    
    # def create_tags(self):
    #     for word in self.body.split():
    #         if (word[0]=='#'):
    #             tag = Tag.objects.filter(name_tag=word[1:]).first()
    #             if tag:
    #                 self.tags.add(tag.pk)
    #             else:
    #                 tag =Tag(name=word[1:])
    #                 tag.save()
    #                 self.tags.add(tag.pk)
    #             self.save()
        
    #     if self.shared_body:
    #         for word in self.shared_body.split():
    #             if (word[0]=='#'):
    #                 tag=Tag.objects.filter(name_tag=word[1:]).first()
    #                 if tag:
    #                     self.tags.add(tag.pk)
    #                 else:
    #                     tag=Tag(name_tag=word[1:])
    #                     tag.save()
    #                     self.tags.add(tag.pk)
    #                 self.save()

    class Meta:
        ordering = ['-date_time', '-shared_on']

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('post_list')

class Comment(models.Model):
    comment=models.TextField()
    date_time=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post=models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    likes=models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes=models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    # tags = models.ManyToManyField('Tag', blank=True)
    
    # def create_tags(self):
    #     for word in self.comment.split():
    #         if (word[0]=='#'):
    #             tag = Tag.objects.get(name_tag=word[1:])
    #             if tag:
    #                 self.tags.add(tag.pk)
    #             else:
    #                 tag=Tag(name_tag=word[1:])
    #                 tag.save()
    #                 self.tags.add(tag.pk)
    #             self.save()

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-date_time').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
        
    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('post_list')


class MaritalStatus(models.Model):
    marital_status=models.CharField(max_length=50)
    def __str__(self):
        return self.marital_status
class Religion(models.Model):
    own_religion=models.CharField(max_length=50)
    def __str__(self):
        return self.own_religion
class Work(models.Model):
    employment=models.CharField(max_length=100)
    def __str__(self):
        return self.employment
class UserProfile(models.Model):
    user=models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name=models.CharField(max_length=30, blank=True, null=True)
    bio=models.TextField(max_length=500, blank=True, null=True)
    location=models.CharField(max_length=100, blank=True, null=True)
    birth_date=models.DateField(blank=True, null=True)
    education=models.CharField(max_length=100, blank=True, null=True)
    work=models.ForeignKey(Work, on_delete=models.CASCADE, blank=True, null=True)
    place_of_work=models.CharField(max_length=200, blank=True, null=True)
    skill=models.CharField(max_length=200, blank=True, null=True)
    hobby=models.CharField(max_length=100, blank=True, null=True)
    religion=models.ForeignKey(Religion, on_delete=models.CASCADE, blank=True, null=True)
    status=models.ForeignKey(MaritalStatus, on_delete=models.CASCADE, blank=True,null=True)
    profile_picture=models.ImageField(upload_to='profile/profile_pictures/', default='profile/profile_pictures/default.png', blank=True)
    followers=models.ManyToManyField(User, blank=True, related_name='followers')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Notification(models.Model):
    # 1 = like, 2=Comment, 3=Follow, 4=inbox 5=shared_post
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    shared_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

# class Image(models.Model):
#     image=models.ImageField(blank=True, null=True, upload_to='post/post_pictures/')

# class Tag(models.Model):
#     name_tag=models.CharField(max_length=255)

class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    

