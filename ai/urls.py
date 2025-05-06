from django.urls import path
from .views import chat_view, register_view, login_view, logout_view, landing_view, upload_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', landing_view, name='landing'),
    path('upload/', upload_view, name='upload'),
    path('chat/', chat_view, name='chat'),
]



