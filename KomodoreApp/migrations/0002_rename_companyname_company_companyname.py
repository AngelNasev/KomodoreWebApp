# Generated by Django 4.2.4 on 2023-08-03 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KomodoreApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='companyname',
            new_name='companyName',
        ),
    ]
