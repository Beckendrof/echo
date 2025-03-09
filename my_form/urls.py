from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home_view, name='home'),
    path('', views.register_view, name='register'),
    path('apply/', views.apply_view, name='apply'),
]
