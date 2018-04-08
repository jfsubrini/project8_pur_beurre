from django.urls import path

from . import views


urlpatterns = [
    # url(r'^$', views.search, name='search'),
    # url(r'^$', views.selection, name='selection'),
    # path(r'^$', views.food, name='food'),    
    path('', views.home, name='home'),
]
