from django.urls import path
from . import views

app_name = 'ai_file'

urlpatterns = [
    path('upload/', views.upload_file, name='file_upload'),
    path('file/<int:pk>/', views.file_detail, name='file_detail'),
    path('', views.file_list, name='file_list'), 
]

