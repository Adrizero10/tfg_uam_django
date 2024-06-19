from django.views.generic import RedirectView
from django.urls import path
from . import views


# Author : Adrian Crespo Musheghyan
#
# Catalog urls
#
urlpatterns = [
    path('', RedirectView.as_view(url='home/'), name='start'),
    path('home/', views.homeView, name='home'),
    path('home/search/', views.homeSearchView, name='search'),
    path('send_informe_phishing/', views.send_mail_phising_warnings, name='send_informe_phishing'),
    path('phishing/', views.phishing, name='phishing'),

]