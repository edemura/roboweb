# Generated by Django 3.2.23 on 2023-11-24 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webadmin', '0008_robo7task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robo7task',
            name='tray_num',
            field=models.IntegerField(default=0, verbose_name='Назначенный лоток'),
        ),
    ]