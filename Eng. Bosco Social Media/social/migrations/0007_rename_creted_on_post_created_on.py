# Generated by Django 4.0.2 on 2022-06-12 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_alter_post_creted_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='creted_on',
            new_name='created_on',
        ),
    ]
