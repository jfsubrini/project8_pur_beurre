"""Food app URL Configuration."""


# Django imports
from django.urls import path, re_path
from django.views.generic import TemplateView

# Import from my app
from . import views



urlpatterns = [
    path('', TemplateView.as_view(template_name='food/home.html'), name='home'),
    path('index/', TemplateView.as_view(template_name='food/home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='food/home.html'), name='home'),
    path('account/', views.account, name='account'),
    path('account/register/', views.register, name='register'),
    path('account/signin/', views.signin, name='signin'),
    path('account/signout/', views.signout, name='signout'),
    path('foodresult/', views.foodresult, name='foodresult'),
    # re_path(r'^foodinfo/(?P<pk>\d+)/$', views.foodinfo, name='foodinfo'),
    re_path(r'^foodinfo/(?P<pk>\d+)/$', views.FoodInfo.as_view(), name='foodinfo'),
    path('selection/', views.selection, name='selection'),
    path('imprint/', TemplateView.as_view(template_name='food/imprint.html'), name='imprint'),
]
