# Generated by Django 3.0.2 on 2020-03-09 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_auto_20200309_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='comments',
            field=models.ManyToManyField(related_name='news_comments', to='news.Comments'),
        ),
    ]
