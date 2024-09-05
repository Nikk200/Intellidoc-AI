from celery import shared_task
import time
from .ocr import extract_text_from_image, extract_text_from_pdf
from documents.models import Document, ExtractedText, AIResult
from documents.ai_processing import analyze_text
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from celery.exceptions import MaxRetriesExceededError


@shared_task(bind=True)
def test_func(self):
    # do something
    for i in range(1, 10):
        time.sleep(5)
        print(i)
    return "Done form celery task"


@shared_task(bind=True, max_retries=3)
def process_document(self, document_id):
    try:
        # Retrieve the document from the database
        document = Document.objects.get(id=document_id)
    except ObjectDoesNotExist as exc: # Handle the case where the document does not exist
        self.retry(exc=e, countdown=5)
        return {'status': 'failure', 'error': 'Document does not exist.'}

    try:
        with transaction.atomic():
            extracted_text = ""
            file_name = document.file.name.lower()

            if file_name.endswith(".pdf"):
                try:
                    extracted_text = extract_text_from_pdf(document.file.path)
                except Exception as e:
                    self.retry(exc=e, countdown=5)
            else:
                try:
                    extracted_text = extract_text_from_image(document.file.path)
                except Exception as e:
                    self.retry(exc=e, countdown=5)

            # Save the extracted text
            if text:
                text = ExtractedText.objects.create(document_id=document_id, text=extracted_text)
            

            # Analyze the text using AI
            ai_result = analyze_text(text.text)
            entities = ai_result.get('entities')
            classification = ai_result.get('classification')
            sentiment = ai_result.get('sentiment')

            # Create AI result
            AIResult.objects.create(
                document=document,
                entity_data = entities,
                classification = classification,
                sentiment = sentiment
            )

            # Update document status to processed
            document.processed = True
            document.save()

        return {'status': 'success', 'message': 'Document processing completed'}
        
    except Exception as e:
        self.retry(exc=e, countdown=5)
        document.status = 'failed'
        document.save()
        raise e



@shared_task(bind=True, max_retries=3)
def add_numbers(self, a, b):
    try:
        result = a + b
        undefined_variable += 1
        print(f"======== The result is: {result}")
        return result
    except Exception as e:
        print(f"Task failed with UnboundLocalError: {e}")
        try:
            raise self.retry(exc=e, countdown=5)
        except MaxRetriesExceededError:
            print("Maximum retries exceeded")
            raise e



