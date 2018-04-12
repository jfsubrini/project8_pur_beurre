from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('index/', views.home, name='home'),    
    path('account/', views.account, name='account'),
    path('credits/', views.credits, name='credits'),
    path('selection/', views.selection, name='selection'),
    url(r'^connexion$', views.connexion, name='connexion'),
]
