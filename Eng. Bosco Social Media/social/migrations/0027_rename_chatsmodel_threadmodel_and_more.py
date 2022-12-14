# Generated by Django 4.0.2 on 2022-08-17 14:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0026_chatsmodel_messagemodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChatsModel',
            new_name='ThreadModel',
        ),
        migrations.RenameField(
            model_name='messagemodel',
            old_name='message_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='messagemodel',
            old_name='chats',
            new_name='thread',
        ),
    ]
