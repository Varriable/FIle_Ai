from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from .forms import UploadFileForm, AskForm
import os


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('file_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.pdf':
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([page.extract_text() for page in reader.pages])
    elif ext == '.docx':
        import docx
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    return "Unsupported file format."

def ask_ai(prompt, context):
    import requests
    response = requests.post(
        "http://localhost:1234/v1/completions",
        json={
            "prompt": f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:",
            "max_tokens": 300,
            "temperature": 0.7
        }
    )
    return response.json()['choices'][0]['text'].strip()

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request, 'ai_work/upload.html', {'form': form})

@login_required
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'ai_work/list.html', {'files': files})

@login_required
def file_detail(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk, user=request.user)
    form = AskForm()
    result = None
    context_text = extract_text(file.file.path)

    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data.get('prompt')
            if 'summarise' in request.POST:
                result = ask_ai("Summarise this document", context_text)
            elif prompt:
                result = ask_ai(prompt, context_text)

    return render(request, 'ai_work/detail.html', {
        'file': file,
        'form': form,
        'result': result,
    })

