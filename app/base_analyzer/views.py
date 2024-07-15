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
        serializer=Model_Serializer_Public(Model.objects.filter(hidden=False, status=3), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user_query=request.data.get('query')
        model=Model.objects.filter(id=request.data.get('model',1)).first()
        if not model:
            return Response({'status':False,'msg':'Model does not exist'}, status=status.HTTP_404_NOT_FOUND)
        cleaned_data={"user_message":user_query, "target_model":model.id}
        classify_ser=Classification_request_Serializer_form(data=cleaned_data)
        if classify_ser.is_valid():
            classify=classify_ser.save()
        else:
            return Response(classify_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        # classify.init_classification()
        classify.init_classification_SYNC()
        return Response({'status':True,'msg':'Classification Started', 'class_id':classify.id, "access_key":classify.secret_key}, status=status.HTTP_201_CREATED)

class Get_classification_status(APIView):
    """
    Gets the classification status (full object) for provided id (?cid=) accompanied with access_token (&access_key=)
    """
    def get(self, request, format=None):
        import time
        time.sleep(10)
        classify = Classification_request.objects.filter(
            id=request.GET.get('cid'), secret_key=request.GET.get('access_key')
        ).first()
        if not classify:
            return Response({'status':False,'msg':'Classification request not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data=Classification_request_Serializer(classify)
            return Response(data.data)

    def post(self, request, format=None):
        return Response({'status':False,'msg':'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

add_new_model_password="SONAEMC-TEST"
#obviously this method for securing anything is ridiculous - but for the purpose of this test it will ensure only me or someone from SONAE can add new models (disk space on the server is limited)
class Add_Model(APIView):
    """

    """
    def get(self, request, format=None):
        return Response({'status':False,'msg':'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        user_query=request.data.get('query')
        model=Model.objects.filter(id=request.data.get('model',1)).first()
        if not model:
            return Response({'status':False,'msg':'Model does not exist'}, status=status.HTTP_404_NOT_FOUND)
        cleaned_data={"user_message":user_query, "target_model":model.id}
        classify_ser=Classification_request_Serializer_form(data=cleaned_data)
        if classify_ser.is_valid():
            classify=classify_ser.save()
        else:
            return Response(classify_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        # classify.init_classification()
        classify.init_classification_SYNC()
        return Response({'status':True,'msg':'Classification Started', 'class_id':classify.id, "access_key":classify.secret_key}, status=status.HTTP_201_CREATED)
