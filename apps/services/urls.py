from django.urls import path
from .views import ServicesSubscribed

urlpatterns = [
    path('subscribed', ServicesSubscribed, name='SubscribedServices'),
]