# Generated by Django 4.2.2 on 2023-07-20 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0029_alter_chat_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='reply_status',
            field=models.CharField(default='empty', max_length=30),
        ),
    ]
