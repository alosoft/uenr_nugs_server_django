# Generated by Django 3.0.2 on 2020-03-09 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_auto_20200309_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='comments',
        ),
    ]
