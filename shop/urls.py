from django.urls import path

from shop import views

urlpatterns = [
    path('shop/order/', views.order),
    path('shop/confirm_payment/', views.confirm),
    path('shop/transaction/', views.set_transaction_id),
]
