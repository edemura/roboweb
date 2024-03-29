# Generated by Django 4.2.7 on 2023-11-03 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webadmin', '0002_configtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('configtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webadmin.configtype')),
            ],
        ),
    ]
