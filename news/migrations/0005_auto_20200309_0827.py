# Generated by Django 3.0.2 on 2020-03-09 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20200308_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='thumbnail',
            field=models.URLField(blank=True, help_text='goto generate page', max_length=500),
        ),
    ]
