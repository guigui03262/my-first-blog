# Generated by Django 2.2.11 on 2020-04-21 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_delete_postlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.BigIntegerField(default=0),
        ),
    ]
