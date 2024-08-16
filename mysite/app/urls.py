from django.urls import path
from . import views

urlpatterns = [
    path('ipphone/', views.ipphone, name="ipphone"),
    path('search/', views.search_numbers, name='playground_numbers_search'),
    path('numbers/', views.numbers, name='numbers')
]
