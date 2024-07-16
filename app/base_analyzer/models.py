from django.db import models
from celery.execute import send_task
import uuid
import secrets


def generate_secret_key():
    '''
    Simple func to generate a secret key to access the classifications
    :return:
    '''
    # Generate a UUID
    unique_id = uuid.uuid4()

    # Generate secure random bytes
    random_bytes = secrets.token_hex(16)

    # Combine UUID and random bytes to form the secret key
    secret_key = f"{unique_id}-{random_bytes}"

    return secret_key


# Create your models here.
model_status=(
    (1,"Processing"),
    (2,"Downloading"),
    (3,"Ready"),
    (0,"Failed"),
)
class Model(models.Model):
    '''
    This represents the AI model being used to classify the text sentiment.
    '''
    date_added=models.DateTimeField(auto_now_add=True)
    public_name=models.CharField(max_length=100)
    real_name=models.CharField(max_length=100)
    hidden=models.BooleanField(default=False)

    status=models.IntegerField(choices=model_status, default=1)

    def validate_and_download_model(self):
        '''
        Download the model, once finished the model will be available on the frontend for selection.
        The validity check to ensure the model is a sentiment analysis model is not very robust, so care should be taken.
        '''
        send_task("base_analyzer.tasks.validate_and_download_model", args=(self.id,))

    def validate_and_download_model_SYNC(self):
        '''
        Use only for testing! can take a long time.
        '''
        from .tasks import validate_and_download_model
        validate_and_download_model(self.id)

classification_status=(
    (1,"Submitted"),
    (2,"Processing"),
    (3,"Complete"),
    (0,"Failed"),
)
class Classification_request(models.Model):
    target_model=models.ForeignKey(Model,on_delete=models.CASCADE)
    user_message=models.TextField()
    status=models.IntegerField(choices=classification_status, default=1)
    model_classification=models.CharField(max_length=100, null=True, blank=True)
    model_classification_score=models.FloatField(null=True, blank=True)

    secret_key=models.CharField(max_length=100,default=generate_secret_key, editable=False)
    #we are not saving sensitive data here so protection is not a priority.

    def init_classification(self):
        '''
        This method initiates the classification process in ASYNC via celery task
        :return:
        '''
        # process_classification_request.delay(self.id)
        send_task("base_analyzer.tasks.process_classification_request", args=(self.id,))
        return
    def init_classification_SYNC(self):
        '''
        This method initiates the classification process in SYNC mode by calling the model directly !DEBUG ONLY!
        :return:
        '''
        from .tasks import process_classification_request
        process_classification_request(self.id)
        return

class GenericErrorLog(models.Model):
    '''
    Used to log any error to the database. usefull when we are not sure what errors to expect and logging them to the database allows for better filtering and search when debugging
    '''
    source=models.CharField(max_length=100)#Usually method where the error happened
    exception=models.CharField(max_length=100)#Python exception raised
    traceback=models.TextField(blank=True)#full error traceback for better debugging.
    
def log_exception(exception, traceback,function):
    '''Helper function to log an exception to the database'''
    obj=GenericErrorLog.objects.create(
        exception=str(exception),
        traceback=traceback,
        source=function,
    )
    return obj.id