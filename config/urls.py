from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/', include('ai_file.urls', namespace='ai_file')),
    path('', include('ai_file.urls')),  # Redirect root to upload page
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='ai_file/auth/login.html'),
         name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]