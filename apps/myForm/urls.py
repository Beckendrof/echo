from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('apply/', views.apply, name='apply'),
    path('register/', views.register, name='register'),
    path('register/submit/', views.register_view, name='register_view'),
    path('apply/submit/', views.apply_view, name='apply_view'),
]
