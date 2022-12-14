# Generated by Django 4.0.2 on 2022-08-12 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0019_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choose_picture', models.ImageField(blank=True, null=True, upload_to='post/post_pictures/')),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='choose_picture',
        ),
        migrations.AddField(
            model_name='post',
            name='choose_picture',
            field=models.ManyToManyField(blank=True, null=True, to='social.Image'),
        ),
    ]
