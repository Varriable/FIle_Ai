from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),                  # default landing page
    path('upload/', views.upload_file, name='upload_file'),       # file upload
    path('file/<int:pk>/', views.file_detail, name='file_detail'),# view/interact with a file
    path('register/', views.register, name='register'),           # user registration
]
