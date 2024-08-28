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
                process_document.delay(doc.id)
        return HttpResponse("file received")
    return HttpResponseBadRequest("Method not allowed.")


@login_required
def documents_list(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'document_list.html', {"documents": documents})
    


def check_document_result(request, task_id):
    
    pass

