from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import FileDocument, FileAnalysis
from .forms import FileUploadForm, AnalysisQueryForm
from django.urls import reverse
import os
from django.contrib import messages
from .ai_utils import analyze_content , extract_text



@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            return redirect('ai_file:file_detail', pk=file.pk)
    else:
        form = FileUploadForm()
    return render(request, 'ai_file/file_upload.html', {'form': form})


@login_required
def file_detail(request, pk):
    file = get_object_or_404(FileDocument, pk=pk, user=request.user)
    analyses = file.fileanalysis_set.order_by('-created_at')
    
    if 'action' in request.GET and request.GET['action'] == 'summarize':
        try:
            text_content = extract_text(file.file.path)
            analysis = analyze_content(text_content)
            
            # Create and save analysis first
            new_analysis = FileAnalysis.objects.create(
                document=file,
                analysis_type='summary',
                response=analysis
            )
            
            # Redirect to the new analysis anchor
            return redirect(reverse('ai_file:file_detail', kwargs={'pk': pk}))
            
        except Exception as e:
            messages.error(request, f"Summary failed: {str(e)}")
            return redirect('file_detail', pk=pk)

    return render(request, 'ai_file/file_detail.html', {
        'file': file,
        'analyses': analyses
    })

@login_required
def file_list(request):
    files = FileDocument.objects.filter(user=request.user)
    return render(request, 'ai_file/file_list.html', {'files': files})


    

