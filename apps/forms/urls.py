from django.urls import path
from .views import FillipForm, Script

urlpatterns = [
    path('fillip', FillipForm, name='FillipForm'),
    path('script', Script, name='Script'),
]

