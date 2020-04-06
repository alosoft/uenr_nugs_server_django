from django.db import models
from news.models import Media

# Create your models here.


class Member(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.OneToOneField(Media, on_delete=models.PROTECT, blank=False)
    position = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, blank=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Bloc(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    logo = models.OneToOneField(
        Media, on_delete=models.CASCADE, related_name='blocs_logo')
    banner = models.OneToOneField(
        Media, on_delete=models.CASCADE, related_name='blocs_banner')
    description = models.TextField(max_length=700, null=False, blank=False)
    contact = models.TextField(max_length=10000, null=True, blank=True)
    history = models.TextField(max_length=10000, null=True, blank=True)
    profile = models.TextField(max_length=10000, null=True, blank=True)
    members = models.ManyToManyField(Member, related_name='bloc_members')
    gallery = models.ManyToManyField(Media, related_name='bloc_gallery')
    website = models.URLField()
    date_established = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.name

    def gallery_list(self):
        gal_list = []
        for item in self.gallery.values():
            gal_list.append(item['image'])

        return gal_list

    def executives(self):
        temp_list = []
        for item in self.members.values():
            whole = {}
            whole['name'] = item['name']
            whole['image'] = Media.objects.get(pk=int(item['image_id'])).image
            whole['position'] = item['position']
            whole['email'] = item['email']
            temp_list.append(whole)
        return temp_list

    def logos(self):
        return self.logo.image

    def banners(self):
        return self.banner.image

    def date(self):
        return self.date_established.strftime('%d %B %Y')
