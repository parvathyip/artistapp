# Generated by Django 4.2.2 on 2023-08-03 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0032_remove_chat_reply_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestproduct',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='requestproduct',
            name='payment_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
