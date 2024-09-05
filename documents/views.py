from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from documents.models import Document
from .task import process_document
from django.views.decorators.http import require_POST
from celery.result import AsyncResult
import os
from django.db.models import Q


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


@login_required
def documents_list(request):
    documents = Document.objects.filter(user=request.user)
    docs = list()
    for doc in documents:
        docs.append({'doc_id': doc.id, 'doc_name':os.path.basename(doc.file.name), 'doc_type': os.path.basename(doc.file.name).split('.')[1], 'uploaded_at': doc.uploaded_at, 'is_processed': doc.processed})
    return render(request, 'documents.html', {"documents": docs})


@login_required
def documents_list_data(request):
    # Capture DataTable parameters from request.GET
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))  # Number of records to return
    search_value = request.GET.get('search[value]', '').strip()  # Search value
    order_column_index = int(request.GET.get('order[0][column]', 0))  # Index of the column to order by
    order_direction = request.GET.get('order[0][dir]', 'asc')  # asc or desc

    # Mapping the column index to actual model fields
    columns = ['id', 'file', 'uploaded_at', 'processed']  # Matches your model fields
    order_column = columns[0]
    
    # Handle ordering direction
    if order_direction == 'desc':
        order_column = '-' + order_column

    documents = Document.objects.filter(user=request.user)
    
    if search_value:
        documents = documents.filter(
            Q(file__icontains=search_value) | Q(uploaded_at__icontains=search_value)
        )
    
    # Total records before filtering
    records_total = documents.count()

    # Apply ordering and pagination
    documents = documents.order_by(order_column)[start:start + length]
    
    docs = [
        {
            'doc_id': doc.id,
            'doc_name': os.path.basename(doc.file.name),
            'doc_type': os.path.basename(doc.file.name).split('.')[1],
            'uploaded_at': doc.uploaded_at,
            'is_processed': doc.processed
        }
        for doc in documents
    ]
    
    return JsonResponse({
        "draw": draw,  # Send back the same draw value
        "recordsTotal": records_total,  # Total number of records (before filtering)
        "recordsFiltered": records_total,  # Total number of records after filtering
        "data": docs  # Actual data to display
    })




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

