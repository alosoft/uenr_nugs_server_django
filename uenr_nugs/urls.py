"""uenr_nugs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from news import views as news_views
from uenr_nugs import settings
from users import views as users_views, urls as user_urls
from shop import views as shop_views, urls as shop_urls
from nugs import views as nugs_views

router = routers.DefaultRouter()
router.register(r'news', news_views.NewsViewSet, basename='news')
router.register(r'comments', news_views.CommentsViewSet, basename='comments')
router.register(r'media', news_views.MediaViewSet, basename='media')
router.register(r'users', users_views.UserViewSet, basename='users')
router.register(r'products', shop_views.ProductViewSet, basename='products')
router.register(r'orders', shop_views.OrderViewSet, basename='orders')
router.register(r'reviews', shop_views.ReviewViewSet, basename='reviews')
router.register(r'orders_item', shop_views.OrderItemViewSet, basename='orders_items')
router.register(r'blocs', nugs_views.BlocViewSet, basename='blocs')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(news_urls)),
    path('api/', include(user_urls)),
    path('api/', include(router.urls)),
    path('api/', include(shop_urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('auth/', include('authapp.urls'))
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
