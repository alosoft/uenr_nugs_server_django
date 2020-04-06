# Generated by Django 3.0.2 on 2020-04-05 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_auto_20200405_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled'), ('Not Paid', 'Not Paid')], default='1', max_length=50),
        ),
    ]
