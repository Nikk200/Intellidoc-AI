from django.contrib import admin
from documents.models import Document, AIResult, ExtractedText


admin.site.register(Document)
admin.site.register(ExtractedText)
admin.site.register(AIResult)