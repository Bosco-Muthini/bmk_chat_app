# Generated by Django 4.0.2 on 2022-06-19 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile/profile_pictures/default.png', upload_to='profile/profile_pictures/'),
        ),
    ]