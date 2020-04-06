# Generated by Django 3.0.2 on 2020-03-15 03:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0002_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.TextField(default='None', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.TextField(default='None', max_length=1000),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(default='Not Paid', max_length=50)),
                ('quantity', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item_owner', to=settings.AUTH_USER_MODEL)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_order_item', to='shop.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Cancelled', 'Cancelled'), ('Not Paid', 'Not Paid')], max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('items', models.ManyToManyField(related_name='user_order', to='shop.OrderItem')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
