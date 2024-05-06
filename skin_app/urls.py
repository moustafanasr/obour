from django.urls import path
from .views import HomePageView,DownloadPDF
app_name = 'skin_app'
    
urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('download-report/',DownloadPDF.as_view(),name='download_pdf')
]