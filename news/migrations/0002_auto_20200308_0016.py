# Generated by Django 3.0.2 on 2020-03-08 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='thumbnail',
            field=models.URLField(blank=True, help_text='goto generate page size=310px X 310px', max_length=100),
        ),
    ]
