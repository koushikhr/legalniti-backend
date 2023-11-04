from django.urls import path
from . import views

urlpatterns = [
    path('', views.trade, name='trade'),
    path('submit',views.submit_form,name='submit')
]