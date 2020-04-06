# Generated by Django 3.0.2 on 2020-03-15 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20200315_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='color_code',
            field=models.CharField(help_text='goto https://htmlcolorcodes.com/color-names/ and pick appropriate color code eg.FF0000 for red', max_length=6, unique=True),
        ),
    ]
