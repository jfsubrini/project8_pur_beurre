"""Food app URL Configuration"""


# Django imports
from django.urls import path, re_path

# Import from my app
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('index/', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('account/register/', views.register, name='register'),
    path('account/signin/', views.signin, name='signin'),
    path('account/signout/', views.signout, name='signout'),
    path('foodresult/', views.foodresult, name='foodresult'),
    re_path(r'^foodinfo/(?P<id_food>[0-9]+)/$', views.foodinfo, name='foodinfo'),
    path('selection/', views.selection, name='selection'),
    path('credits/', views.credits, name='credits'),
]
