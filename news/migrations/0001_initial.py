# Generated by Django 3.0.2 on 2020-03-07 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('media_type', models.CharField(choices=[('Video', 'Video'), ('Picture', 'Picture')], default='Picture', max_length=20)),
                ('image', models.URLField(blank=True, help_text='goto generate page', max_length=100)),
                ('thumbnail', models.URLField(blank=True, default='https://i.imgur.com/6k3PK8n.png', help_text='goto generate page size=310px X 310px', max_length=100)),
                ('video', models.URLField(blank=True, help_text='copy video link from youtube, eg "https://www.youtube.com/embed/EreZNkWzBAw', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Media',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Leadership', 'Leadership'), ('General', 'General'), ('Campus', 'Campus'), ('Security', 'Security'), ('Health', 'Health'), ('Entertainment', 'Entertainment'), ('Activities', 'Activities'), ('Religion', 'Religion')], max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(max_length=2000)),
                ('image', models.ManyToManyField(related_name='news_image', to='news.Media')),
            ],
            options={
                'verbose_name_plural': 'News',
                'ordering': ['created'],
            },
        ),
    ]
