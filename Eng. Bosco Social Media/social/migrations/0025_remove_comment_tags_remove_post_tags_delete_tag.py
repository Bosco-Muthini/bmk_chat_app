# Generated by Django 4.0.2 on 2022-08-16 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0024_tag_comment_tags_post_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]