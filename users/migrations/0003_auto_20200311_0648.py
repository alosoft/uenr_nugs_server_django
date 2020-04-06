# Generated by Django 3.0.2 on 2020-03-11 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_price'),
        ('users', '0002_auto_20200307_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cart',
            field=models.ManyToManyField(blank=True, related_name='user_carts', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='user',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='user_favorite', to='shop.Product'),
        ),
    ]