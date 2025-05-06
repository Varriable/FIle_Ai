# views.py
import os
import json
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def landing_view(request):
    return render(request, 'landing.html')

# Registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def upload_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Save metadata
        UploadedFile.objects.create(
            user=request.user,
            file=filename,
            original_name=uploaded_file.name
        )
        return redirect('upload')

    user_files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'upload.html', {'files': user_files})

# Chat Page
@login_required
def chat_view(request):
    user_files = UploadedFile.objects.filter(user=request.user)

    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        file_id = request.POST.get('file_id')

        if not file_id:
            return render(request, 'chat.html', {
                'files': user_files,
                'error': 'Please select a file before submitting a prompt.'
            })

        file = UploadedFile.objects.get(id=file_id, user=request.user)
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Standard AI call (no restrictions)
        payload = {
            "messages": [
                {"role": "system", "content": f"You can refer to this file content:\n\n{file_content[:1000]}"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }

        try:
            response = requests.post("http://localhost:1234/v1/chat/completions", headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            reply = response.json()['choices'][0]['message']['content']
        except Exception as e:
            reply = f"Error contacting AI: {e}"

        return render(request, 'chat.html', {
            'files': user_files,
            'reply': reply,
            'selected_file': file,
            'prompt': prompt
        })

    return render(request, 'chat.html', {'files': user_files})


