from django.urls import path
from . import views
from .views import Ipphone

urlpatterns = [
    path('ipphone/', Ipphone.as_view()),
    path('', Ipphone.as_view()),
    path('numbers/', views.numbers, name='numbers')
]
