from django.db import models
from django.contrib.auth.models import User

class FileDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FileAnalysis(models.Model):
    document = models.ForeignKey(FileDocument, on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=50)
    query = models.TextField(null=True, blank=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document.title} - {self.analysis_type}"