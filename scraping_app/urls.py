from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scrape-data/', views.scrape_data_view, name='scrape_data'),
    path('get-data/', views.get_data, name='get_data'),
]
