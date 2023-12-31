# Generated by Django 4.2.4 on 2023-08-22 23:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('KomodoreApp', '0005_product_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KomodoreApp.product')),
            ],
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='cart_items',
            field=models.ManyToManyField(to='KomodoreApp.cartitem'),
        ),
    ]
