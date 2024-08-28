from celery import shared_task
import time
from .ocr import extract_text_from_image, extract_text_from_pdf
from documents.models import Document, ExtractedText, AIResult
from documents.ai_processing import analyze_text
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

@shared_task(bind=True)
def test_func(self):
    # do something
    for i in range(1, 10):
        time.sleep(5)
        print(i)
    return "Done form celery task"


@shared_task(bind=True)
def process_document(self, document_id):
    try:
        # Retrieve the document from the database
        document = Document.objects.get(id=document_id)
    except ObjectDoesNotExist: # Handle the case where the document does not exist
        # self.update_state(state='FAILURE', meta={'exc_type': type(e), 'exc_message': str(e)})
        return {'status': 'failure', 'error': 'Document does not exist.'}

    try:
        with transaction.atomic():
            extracted_text = ""
            file_name = document.file.name.lower()

            if file_name.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(document.file.path)
            else:
                extracted_text = extract_text_from_image(document.file.path)

            # Save the extracted text
            text = ExtractedText.objects.create(document_id=document_id, text=extracted_text)
            

            # Analyze the text using AI
            print("before analyze text function >>", text.text)
            ai_result = analyze_text(text.text)
            entities = ai_result.get('entities')
            classification = ai_result.get('classification')
            sentiment = ai_result.get('sentiment')
            print("after AI analysis >>")

            # Update or create AI result
            ai_result_obj, created = AIResult.objects.update_or_create(
                document=document,
                defaults={
                    'entity_data': entities,
                    'classification': classification,
                    'sentiment': sentiment,
                }
            )

            # Update document status to processed
            document.status = 'processed'
            document.save()

        return {'status': 'success', 'message': 'Document processing completed'}
        
    except Exception as e:
        # Handle any errors that occur during processing
        # self.update_state(state='FAILURE', meta={'error': str(e)})
        # self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e)})
        document.status = 'failed'
        document.save()
        return {'status': 'failure', 'error': str(e)}
        