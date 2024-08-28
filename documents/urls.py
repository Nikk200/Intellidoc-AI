from django.urls import path
from documents import views

app_name = "documents"


urlpatterns = [
    path("upload-document", views.upload_document, name='upload-document'),
    path("documents-list", views.documents_list, name='documents-list')
]
