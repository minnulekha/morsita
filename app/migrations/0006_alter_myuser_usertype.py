# Generated by Django 5.2.3 on 2025-06-25 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_menuitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='usertype',
            field=models.CharField(choices=[('customer', 'Customer'), ('restaurant', 'Restaurant Staff'), ('delivery', 'Delivery Partner')], max_length=20),
        ),
    ]
