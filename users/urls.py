from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from users import views

urlpatterns = [
    path('users/update/', views.update),
    path('users/cart/', views.cart),
    path('users/favorite/', views.favorite),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
