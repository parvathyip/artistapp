# Generated by Django 4.2.2 on 2023-07-19 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0023_product_prodstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestproduct',
            name='reqexpecteddate',
            field=models.DateField(null=True),
        ),
    ]