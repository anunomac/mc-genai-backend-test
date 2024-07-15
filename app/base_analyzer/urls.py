from .views import *
from django.urls import path

urlpatterns = [
    # path("file_cat/", file_categorization.as_view()),
    path("", Sentiment_analyzer_view.as_view(), name="home"),
    path("get_status/", Get_classification_status.as_view(), name="get_query_status"),
    ]