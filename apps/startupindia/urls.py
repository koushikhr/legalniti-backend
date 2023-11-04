from django.urls import path
from . import views

urlpatterns = [
    path('login', views.stratup_login, name='login'),
    path('form',views.startup,name='form'),
    path('submit',views.form_submit,name='submit')
]