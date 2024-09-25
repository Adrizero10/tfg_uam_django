from django.views.generic import RedirectView
from django.urls import include, path
from . import views


# Author : Adrian Crespo Musheghyan
#
# Catalog urls
#
urlpatterns = [
    path('', RedirectView.as_view(url='home/'), name='start'),
    path('home/', views.homeView, name='home'),
    path('detail/', views.detailView, name='detail'),
    path('', include('authentication.urls')),
]