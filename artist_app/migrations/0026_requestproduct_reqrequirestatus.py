# Generated by Django 4.2.2 on 2023-07-19 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0025_requestproduct_reqcompletedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestproduct',
            name='reqrequirestatus',
            field=models.CharField(default='Pending', max_length=30),
        ),
    ]