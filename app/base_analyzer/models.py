from django.db import models

# Create your models here.
class Model(models.Model):
    '''
    For the purposes of this test, only one model will be used, however it would be possible to provide more models for users to use.
    '''
    date_added=models.DateTimeField(auto_now_add=True)
    public_name=models.CharField(max_length=100)
    real_name=models.CharField(max_length=100)
    hidden=models.BooleanField(default=False)

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
    model_classification=models.CharField(max_length=100)

    def init_classification(self):
        return