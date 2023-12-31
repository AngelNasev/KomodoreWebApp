# Generated by Django 4.2.4 on 2023-08-25 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KomodoreApp', '0007_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Online', 'Online'), ('Cash', 'Cash on Delivery')], default='Pending', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=20),
            preserve_default=False,
        ),
    ]
