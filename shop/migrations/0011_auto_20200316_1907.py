# Generated by Django 3.0.2 on 2020-03-16 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20200315_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Cancelled', 'Cancelled'), ('Not Paid', 'Not Paid')], default='Not Paid', max_length=50),
        ),
    ]
