# Generated by Django 3.0.2 on 2020-03-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_auto_20200309_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='news_comments', to='news.Comments'),
        ),
    ]
