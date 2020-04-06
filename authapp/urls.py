from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

# from users import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
