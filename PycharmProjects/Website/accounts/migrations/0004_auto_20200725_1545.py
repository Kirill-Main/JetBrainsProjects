# Generated by Django 3.0.8 on 2020-07-25 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200725_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='product_image',
            new_name='product',
        ),
    ]
