from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('', views.character_list, name='character_list'),
    path('character/<str:pk>/', views.character_detail, name='character_detail'),
    path('equipement/<str:pk>/', views.equipement_detail, name='equipement_detail'),
    path('character/<str:pk>/?<str:message>', views.character_detail, name='character_detail_mes'),
]