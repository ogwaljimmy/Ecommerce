from django.urls import path
from . import views
from .webhooks import flutterwave_webhook


urlpatterns = [

    path('checkout', views.checkout, name='checkout'),
    path('complete-order', views.complete_order, name='complete-order'),
    path('payment-success', views.payment_success, name='payment-success'),
    path('payment-failed', views.payment_failed, name='payment-failed'),
    path('verify-mobile-money/', views.verify_mobile_money, name='verify-mobile-money'),
    path('flutterwave-webhook/', flutterwave_webhook, name='flutterwave-webhook'),

]








