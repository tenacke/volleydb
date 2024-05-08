from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('add_player', views.add_player, name='add_player'),
    path('add_coach', views.add_coach, name='add_coach'),
    path('add_jury', views.add_jury, name='add_jury'),
]