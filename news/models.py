from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from django.urls import reverse
from django.utils.html import format_html
from uenr_nugs import settings
import datetime
from django.utils import timezone
import math


class Media(models.Model):
    type = (
        ('Video', 'Video'),
        ('Picture', 'Picture')
    )
    title = models.CharField(max_length=50, blank=False)
    media_type = models.CharField(
        choices=type, max_length=20, default='Picture')
    image = models.URLField(max_length=500, blank=True,
                            help_text='goto generate page')
    thumbnail = models.URLField(max_length=500, blank=True,
                                help_text='goto generate page')
    video = models.URLField(max_length=100, blank=True,
                            help_text='copy video link from youtube, eg "https://www.youtube.com/embed/EreZNkWzBAw')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Media'

    def __str__(self):
        return self.title

    def image_preview(self):
        return format_html(f'<a href="{self.image}" target="_blank"> <img src="{self.image}" height=60px/></a>')

    def clean(self):
        if self.media_type == 'Picture' and self.video.__len__() > 0:
            raise ValidationError(
                _("Only video Media Type can have a video link"))
        if self.media_type == 'Video' and self.video.__len__() < 1:
            raise ValidationError(_("Videos should have a video link"))

    image_preview.admin_order_field = 'image'


class Comments(models.Model):
    body = models.TextField(blank=False, max_length=700)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    approved = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "owner"), on_delete=models.CASCADE, editable=False)
    news_id = models.IntegerField(blank=False, editable=False)

    def __str__(self):
        return 'Comment by {}'.format(self.owner)

    class Meta:
        verbose_name_plural = 'Comments'

    # def date(self):
    #     diff = datetime.datetime.utcnow() - self.created.utcnow()
    #     s = diff.seconds
    #     if diff.days > 7 or diff.days < 0:
    #         return self.created.strftime('%a, %d %B %Y')
    #     elif diff.days == 1:
    #         return '1 day ago'
    #     elif diff.days > 1:
    #         return '{} days ago'.format(diff.days)
    #     elif s <= 1:
    #         return 'just now'
    #     elif s < 60:
    #         return '{} seconds ago'.format(s)
    #     elif s < 120:
    #         return '1 minute ago'
    #     elif s < 3600:
    #         return '{} minutes ago'.format(s / 60)
    #     elif s < 7200:
    #         return '{} 1 hour ago'
    #     else:
    #         return '{} hours ago'.format(s / 3600)

    def date(self):
        now = timezone.now()

        diff = now - self.created

        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds

            return 'just now'

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if 1 <= diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if 30 <= diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

        # return self.created.strftime('%a, %d %B %Y')


class News(models.Model):
    cat = (
        ('Leadership', 'Leadership'),
        ('General', 'General'),
        ('Campus', 'Campus'),
        ('Security', 'Security'),
        ('Health', 'Health'),
        ('Entertainment', 'Entertainment'),
        ('Activities', 'Activities'),
        ('Religion', 'Religion')
    )

    title = models.CharField(max_length=200, null=False, blank=False)
    category = models.CharField(
        choices=cat, max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)
    image = models.ManyToManyField(Media, blank=False, unique=False,
                                   related_name='news_image')
    comments = models.ManyToManyField(Comments, blank=False, unique=False,
                                      related_name='news_comments')
    body = models.TextField(max_length=10000, null=False, blank=False)

    def comments_count(self):
        return self.comments.all().__len__()

    def date(self):
        return self.created.strftime('%a, %d %B %Y')
        # return self.created.strftime("%d-%m-%Y")

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['created']

    def __str__(self):
        return self.title

    def images(self):
        images = []
        for item in self.image.values():
            if item['media_type'] == 'Picture':
                images.append(item['image'])
            if item['media_type'] == 'Video':
                images.append(item['video'])
        return images
