# Generated by Django 3.0.8 on 2020-07-25 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200725_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='published',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления'),
        ),
    ]
