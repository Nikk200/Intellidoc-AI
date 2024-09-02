from django.urls import path
from documents import views

app_name = "documents"


urlpatterns = [
    path("upload-document", views.upload_document, name='upload-document'),
    path("documents-list", views.documents_list, name='documents-list'),
    path("check-document-result/<str:task_id>/", views.check_document_result, name='check-document-result'),
]
