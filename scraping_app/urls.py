from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scrape-data/', views.scrape_data_view, name='scrape_data'),
    path('get-data/', views.get_data, name='get_data'),
    path('download-page/<str:filename>/', views.download_page, name='download_page'),
    path('download-file/<str:filename>/', views.download_file, name='download_file'),
    path('cancel-download/<str:filename>/', views.cancel_download, name='cancel_download'),

]
