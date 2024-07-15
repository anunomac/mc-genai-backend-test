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
    For the purposes of this test, only one model will be used, however it would be possible to provide more models for users to use.
    '''
    date_added=models.DateTimeField(auto_now_add=True)
    public_name=models.CharField(max_length=100)
    real_name=models.CharField(max_length=100)
    hidden=models.BooleanField(default=False)

    status=models.IntegerField(choices=model_status, default=1)

    def validate_and_download_model(self):
        send_task("base_analyzer.tasks.validate_and_download_model", args=(self.id,))

    def validate_and_download_model_SYNC(self):
        from .tasks import validate_and_download_model
        validate_and_download_model(self.id)

            # languages=models.CharField(max_length=100)
# class Sentiment_LOG(models.Model):
#     '''
#     Logs the user submitted sentiment request and classification by the model
#     '''
#     date_added=models.DateTimeField(auto_now_add=True)
#     model_used=models.ForeignKey(Model,on_delete=models.CASCADE)
#     user_message=models.TextField()
#     model_classification=models.CharField(max_length=100)

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
