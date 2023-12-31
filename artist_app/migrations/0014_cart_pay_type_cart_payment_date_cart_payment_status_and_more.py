# Generated by Django 4.2.2 on 2023-07-18 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0013_cart_cart_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='pay_type',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='cart',
            name='payment_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='payment_status',
            field=models.CharField(default='Pending', max_length=30),
        ),
        migrations.AddField(
            model_name='cart',
            name='qty',
            field=models.CharField(default='1', max_length=30),
        ),
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.CharField(default='0', max_length=30),
        ),
    ]
