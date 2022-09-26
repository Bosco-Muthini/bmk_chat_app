# Generated by Django 4.0.2 on 2022-06-19 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('social', '0009_alter_comment_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marital_status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('own_religion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employment', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('name', models.CharField(max_length=30)),
                ('bio', models.TextField(blank=True, max_length=500, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('education', models.CharField(blank=True, max_length=100, null=True)),
                ('place_of_work', models.CharField(blank=True, max_length=200, null=True)),
                ('skill', models.CharField(blank=True, max_length=200, null=True)),
                ('hobby', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_picture', models.ImageField(blank=True, default='post/profile_pictures/default.png', upload_to='post/profile_pictures/')),
                ('religion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.religion')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.maritalstatus')),
                ('work', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.work')),
            ],
        ),
    ]
