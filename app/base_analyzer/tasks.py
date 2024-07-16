from celery import shared_task
from transformers import pipeline as hf_pipeline
from django.db import transaction
from .models import Classification_request, Model, log_exception
import requests
import traceback



@shared_task
def process_classification_request(request_id):
    print(f"[LOG] Start processing classification request {request_id}")
    classification_request = Classification_request.objects.select_for_update().get(id=request_id)
    try:
        # a=1/0 #force error
        with transaction.atomic():
            classification_request.status = 2  # Processing
            classification_request.save()

            target_model = classification_request.target_model
            sentiment_node = create_sentiment_node(target_model.real_name)

            result = sentiment_node(classification_request.user_message)
            sentiment_label = result[0]['label']
            sentiment_score = result[0]['score']

            print(f"[LOG] classification complete. full response: {result}")
            # print(result)

            classification_request.model_classification = sentiment_label
            classification_request.model_classification_score = sentiment_score
            classification_request.status = 3  # Complete
            classification_request.save()

    except Exception as e:
        classification_request.status = 0  # Failed
        classification_request.save()
        err_id=log_exception(e,traceback.format_exc(),'process_classification_request')
        print(f"[LOG] Model setup for {classification_request} failed! error id: {err_id}")
        raise e
    return

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


    except Exception as e:
        log_exception(e,traceback.format_exc(),'process_classification_request_with_callback')
        raise e
    return


def create_sentiment_node(model_name: str):
    '''helper function'''
    sentiment_model = hf_pipeline("sentiment-analysis", model=model_name)
    return sentiment_model


@shared_task
def validate_and_download_model(model_id):
    internal_model = Model.objects.filter(id=model_id).first()
    print(f"[LOG] Starting setup for {internal_model.real_name}")
    model_name=internal_model.real_name
    internal_model.status = 2
    internal_model.save()
    try:

        print(f"[LOG] Starting download: {internal_model.real_name}")
        sentiment_pipeline = hf_pipeline('sentiment-analysis', model=model_name)

        print(f"[LOG] Starting test: {internal_model.real_name}")
        sentiment_pipeline("Test")
        internal_model.status = 3
        internal_model.save()

        print(f"[LOG] Model setup complete: {internal_model.real_name}")
    except Exception as e:
        internal_model.status = 0
        internal_model.save()
        err_id=log_exception(e,traceback.format_exc(),'process_classification_request')
        print(f"[LOG] Model setup for {internal_model.real_name} failed! error id: {err_id}")
        raise e
    return