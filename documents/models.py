from django.db import models
from django.contrib.auth.models import User



class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='users_documents/')
    processed = models.BooleanField(default=False)  # Flag to indicate if processed

    def __str__(self):
        return f"{self.file.name} uploaded by {self.user.username} on {self.uploaded_at}"


class ExtractedText(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    text = models.TextField(null=True)

    def __str__(self):
        return f"Extracted text for {self.document.file.name}"


class AIResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    entity_data = models.JSONField(blank=True)  # Store Named Entity Recognition (NER) results
    classification = models.CharField(max_length=255, blank=True)  # Document text classification
    sentiment = models.CharField(max_length=50, blank=True)  # Sentiment analysis result

    def __str__(self):
        return f"AI results for {self.document.file.name}"
