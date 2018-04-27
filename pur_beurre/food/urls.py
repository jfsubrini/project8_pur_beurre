"""Food app URL Configuration"""


from django.urls import path, re_path

from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('index/', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('account/register/', views.register, name='register'),
    path('account/login/', views.login, name='login'),
    path('account/logout/', views.logout, name='logout'),
    path('foodresult/', views.foodresult, name='foodresult'),
    re_path(r'^foodinfo/(?P<id_food>[0-9]+)/$', views.foodinfo, name='foodinfo'),
    path('selection/', views.selection, name='selection'),
    path('credits/', views.credits, name='credits'),
]
