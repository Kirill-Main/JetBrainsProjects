# Generated by Django 3.0.8 on 2020-07-05 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200705_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='is_main',
            field=models.BooleanField(default=False, verbose_name='Главный?'),
        ),
    ]