"""Food app URL Configuration"""


from django.urls import path

from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('index/', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('connexion/', views.connexion, name='connexion'),
    path('foodresult/', views.foodresult, name='foodresult'),
    path('foodinfo/', views.foodinfo, name='foodinfo'),
    path('selection/', views.selection, name='selection'),
    path('credits/', views.credits, name='credits'),
]
