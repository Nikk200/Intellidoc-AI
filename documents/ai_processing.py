from transformers import pipeline

ner = pipeline('ner', aggregation_strategy = 'simple') #pipeline for NER
classifier = pipeline("text-classification") #pipeline for text classification
sentiment_analyzer = pipeline("sentiment-analysis") #pipeline for sentiment analysis


def extract_entities(text):
    try:
        # Call the NER pipeline
        doc = ner(text)
        
        # Extract entities from the returned list of dictionaries
        entities = [(entity['word'], entity['entity_group']) for entity in doc]
        return entities
    except Exception as e:
        print("exception >> ", e)
        return None


def classify_text(text):
    classification = ""
    try:
        classification = classifier(text)
    except:
        pass
    return classification


def analyze_sentiment(text):
    sentiment = ""
    try:
        sentiment = sentiment_analyzer(text)
    except:
        pass
    return sentiment

def analyze_text(text):
    entities = extract_entities(text)
    classification = classify_text(text)
    sentiment = analyze_sentiment(text)
    return {
        'entities': entities,
        'classification': classification,
        'sentiment': sentiment
    }