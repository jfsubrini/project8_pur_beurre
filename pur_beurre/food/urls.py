from django.urls import path

from . import views


urlpatterns = [
    # url(r'^$', views.search, name='search'),
    # url(r'^$', views.selection, name='selection'),
    # path(r'^$', views.food, name='food'),    
    path('', views.home, name='home'),
    path('credits/', views.credits, name='credits'),
    path('account/', views.account, name='account'),
    # path('', views.home, name='home'),
    # path('', views.home, name='home'),
    # path('', views.home, name='home'),
]
