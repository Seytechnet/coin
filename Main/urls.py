from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('wallets', views.wallets, name='wallets'),
    path('importkey', views.importkey , name='importkey'),
    path('reference/', views.reference, name='reference'),
]
