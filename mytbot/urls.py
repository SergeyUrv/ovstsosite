from django.urls import path
from django.urls import include
from django.urls import include

from .views import get_temp

urlpatterns = [
    path('get_temp/', get_temp, name='get_temp'),
]