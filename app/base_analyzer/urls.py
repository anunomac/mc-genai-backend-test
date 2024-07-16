from .views import *
from django.urls import path

urlpatterns = [
    # path("file_cat/", file_categorization.as_view()),
    # path("", Sentiment_analyzer_view.as_view(), name="home"),
    path("models/", Get_Models.as_view(), name="models"),
    path("classifications/", Get_classification.as_view(), name="classifications"),
    # path("get_status/", Get_classification_status.as_view(), name="get_query_status"),
    # path("add_model/", Add_Model.as_view(), name="add_model"),
    ]