# Generated by Django 4.0.2 on 2022-08-20 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0028_notification_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='shared_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='social.post'),
        ),
    ]
