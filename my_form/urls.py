from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('', views.apply, name='apply')
]
