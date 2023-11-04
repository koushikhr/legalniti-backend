from django.urls import path
from .views import name_gen
urlpatterns = [
    path('namegenerator',name_gen,name="namegen")
]
