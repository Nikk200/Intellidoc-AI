from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from documents.models import Document
from .task import process_document
from django.views.decorators.http import require_POST
from celery.result import AsyncResult


@login_required
@require_POST
def upload_document(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if file:
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
            if file.name.lower().endswith(tuple(allowed_extensions)):
                doc = Document(user=request.user, file=file)
                doc.save()
                task = process_document.delay(doc.id)

        return HttpResponse(task.id)
    return HttpResponseBadRequest("Method not allowed.")

import os
@login_required
def documents_list(request):
    documents = Document.objects.filter(user=request.user)
    docs = list()
    for doc in documents:
        docs.append({'doc_id': doc.id, 'doc_name':os.path.basename(doc.file.name), 'doc_type': os.path.basename(doc.file.name).split('.')[1], 'uploaded_at': doc.uploaded_at, 'is_processed': doc.processed})
    return render(request, 'documents.html', {"documents": docs})



def check_document_result(request, task_id):
    result = AsyncResult(task_id)
    if result.ready():
        try:
            task_result = result.get()
            return HttpResponse()
        except Exception as e:
            return HttpResponseBadRequest("Task error "+e)
    else:
        return HttpResponseBadRequest("The task is still running, pending, or is waiting for retry")

