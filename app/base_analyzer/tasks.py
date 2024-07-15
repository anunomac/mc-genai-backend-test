from celery import shared_task
from transformers import pipeline as hf_pipeline
from django.db import transaction
from .models import Classification_request, Model
import requests

@shared_task
def process_classification_request(request_id):
    try:
        with transaction.atomic():
            classification_request = Classification_request.objects.select_for_update().get(id=request_id)
            classification_request.status = 2  # Processing
            classification_request.save()

            target_model = classification_request.target_model
            sentiment_node = create_sentiment_node(target_model.real_name)

            result = sentiment_node(classification_request.user_message)
            sentiment_label = result[0]['label']
            sentiment_score = result[0]['score']
            # print(result)

            classification_request.model_classification = sentiment_label
            classification_request.model_classification_score = sentiment_score
            classification_request.status = 3  # Complete
            classification_request.save()

    except Exception as e:
        # todo LOG exception
        classification_request.status = 0  # Failed
        classification_request.save()
        raise e

@shared_task
def process_classification_request_with_callback(query,model,callback_url):
    '''
    This version of the classification function is for external backends (like a node backend) to ask for classification, providing a callback link to post the classification results
    :param query: User query to classify;
    :param query: Model to use;
    :param callback_url: url to post results to;
    :return:
    '''
    try:
        with transaction.atomic():
            target_model = model
            sentiment_node = create_sentiment_node(target_model)

            result = sentiment_node(query)
            sentiment_label = result[0]['label']
            sentiment_score = result[0]['score']
            # print(result)
            requests.post(callback_url,json={"label":sentiment_label,"score":sentiment_score})
            return

    except Exception as e:
        #todo LOG exception
        raise e


def create_sentiment_node(model_name: str):
    sentiment_model = hf_pipeline("sentiment-analysis", model=model_name)
    return sentiment_model


@shared_task
def validate_and_download_model(model_id):
    internal_model = Model.objects.filter(id=model_id).first()
    model_name=internal_model.real_name
    internal_model.status = 2
    internal_model.save()
    try:
        # Attempt to load the model and tokenizer
        # model = AutoModelForSequenceClassification.from_pretrained(model_name)
        # tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Check if the model can be used for sentiment analysis & Download model
        sentiment_pipeline = hf_pipeline('sentiment-analysis', model=model_name)

        sentiment_pipeline("Test")
        internal_model.status = 3
        internal_model.save()

    except Exception as e:
        internal_model.status = 0
        internal_model.save()
        raise e
    return