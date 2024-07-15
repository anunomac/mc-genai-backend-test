from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Model, Classification_request
from .serializers import *


class Sentiment_analyzer_view(APIView):
    """
    Gets all available sentiment analyzers (GET);
    Initiates a new sentiment analysis (POST);
    """
    def get(self, request, format=None):
        #serialize all models
        #return all available models
        serializer=Model_Serializer(Model.objects.filter(hidden=False), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user_query=request.POST.get('query')
        model=Model.objects.filter(id=request.POST.get('model',1)).first()
        if not model:
            return Response({'status':False,'msg':'Model does not exist'}, status=status.HTTP_404_NOT_FOUND)
        classify=Classification_request.objects.create(
            model=request.POST.get('model',1),
            user_query=user_query,
        )
        classify.init_classification()
        return Response({'status':True,'msg':'Classification Started', 'class_id':classify.id}, status=status.HTTP_201_CREATED)

class Get_classification_status(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        classify = Classification_request.objects.filter(
            id=request.POST.get('cid')
        ).first()
        if not classify:
            return Response({'status':False,'msg':'Classification request not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data=Classification_request_Serializer(classify)
            return Response(data.data)

    def post(self, request, format=None):
        return Response({'status':False,'msg':'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)