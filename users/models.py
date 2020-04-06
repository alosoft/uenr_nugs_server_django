from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from news.models import News
from shop.models import Product


class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    image = models.ImageField(blank=True, null=True)
    number = models.CharField(max_length=15, blank=True, null=True)
    bookmarks = models.ManyToManyField(News, blank=True, unique=False,
                                       related_name='user_bookmarks')
    cart = models.ManyToManyField(Product, blank=True, unique=False,
                                  related_name='user_carts')
    favorite = models.ManyToManyField(Product, blank=True, unique=False,
                                      related_name='user_favorite')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name_plural = 'User Accounts'
    
    def __str__(self):
        return self.email

    def get_username(self):
        return self.email
