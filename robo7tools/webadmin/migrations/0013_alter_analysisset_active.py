# Generated by Django 3.2.23 on 2023-11-25 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webadmin', '0012_analysisset_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisset',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Активный набор'),
        ),
    ]
