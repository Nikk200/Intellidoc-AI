# import spacy
from transformers import pipeline

# nlp = spacy.load("en_core_web_sm")
ner = pipeline('ner', aggregation_strategy = 'simple') #pipeline for NER
classifier = pipeline("text-classification") #pipeline for text classification
sentiment_analyzer = pipeline("sentiment-analysis") #pipeline for sentiment analysis


def extract_entities(text):
    print("inside extract_entities >> ", text)

    try:
        # Call the NER pipeline
        doc = ner(text)
        print("after NER >> ", doc)
        
        # Extract entities from the returned list of dictionaries
        entities = [(entity['word'], entity['entity_group']) for entity in doc]
        
        return entities
    except Exception as e:
        print("exception >> ", e)
        return None


def classify_text(text):
    print("classify_text >> ")
    classification = classifier(text)
    return classification


def analyze_sentiment(text):
    print("analyze_sentiment >> ")
    sentiment = sentiment_analyzer(text)
    return sentiment

def analyze_text(text):
    entities = extract_entities(text)
    classification = classify_text(text)
    sentiment = analyze_sentiment(text)
    print("analysis >> ", entities)
    print("analysis >> ", classification)
    print("analysis >> ", sentiment)
    return {
        'entities': entities,
        'classification': classification,
        'sentiment': sentiment
    }