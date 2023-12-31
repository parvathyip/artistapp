# Generated by Django 4.2.2 on 2023-07-18 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0015_cart_order_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(max_length=30)),
                ('cart_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='artist_app.cart')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='artist_app.userreg')),
            ],
        ),
    ]
