from django.urls import path
from .views import login, signup, refresh

urlpatterns = [
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('refresh', refresh, name='refresh')
]
