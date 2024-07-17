from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Model, Classification_request, log_exception
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

add_new_model_password="SONAEMC-TEST"
#obviously this method for securing anything is ridiculous - but for the purpose of this test it will ensure only me or someone from SONAE can add new models (disk space is limited)

class Get_Models(APIView):
    """
    Gets all available sentiment analyzers (GET);
    Attempts to add a new sentiment analyzer (POST);
    """

    @swagger_auto_schema(
        responses={200: Model_Serializer_Public(many=True)}
    )
    def get(self, request, format=None):
        serializer=Model_Serializer_Public(Model.objects.filter(hidden=False, status=3), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password to add new model'),
                'public_name': openapi.Schema(type=openapi.TYPE_STRING, description='Public name of the model'),
                'real_name': openapi.Schema(type=openapi.TYPE_STRING, description='Real name of the model'),
            },
            required=['public_name', 'real_name', 'password'],
        ),
        responses={
            200: 'Model queued for download.',
            400: 'Bad Request - invalid form',
            401: 'Not allowed'
        }
    )
    def post(self, request, format=None):
        # print(request.data)
        password = request.data.get('password')
        if password != add_new_model_password:
            return Response({'status': False, 'msg': 'Not allowed'}, status=status.HTTP_401_UNAUTHORIZED)
        new_model = Model_Serializer(data=request.data)
        if new_model.is_valid():
            obj = new_model.save()
            obj.validate_and_download_model()
            return Response({'status': True, 'msg': 'Model queued for download.'}, status=status.HTTP_200_OK)
        else:
            return Response(new_model.errors, status=status.HTTP_400_BAD_REQUEST)
class Get_classification(APIView):
    """
    Gets the classification status (full object) for provided id (?cid=) accompanied with access_token (&access_key=) (GET)
    Posts a new query for analysis (POST)
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('cid', openapi.IN_QUERY, description="Classification request ID",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('access_key', openapi.IN_QUERY, description="Access key", type=openapi.TYPE_STRING)
        ],
        required=['cid', 'access_key'],
        responses={
            200: Classification_request_Serializer(),
            404: 'Classification request not found'
        }
    )
    def get(self, request, format=None):
        # import time
        # time.sleep(10)
        classify = Classification_request.objects.filter(
            id=request.GET.get('cid'), secret_key=request.GET.get('access_key')
        ).first()
        if not classify:
            return Response({'status':False,'msg':'Classification request not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            data=Classification_request_Serializer(classify)
            return Response(data.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'query': openapi.Schema(type=openapi.TYPE_STRING, description='User query for sentiment analysis'),
                'model': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the model to use'),
            },
            required=['query']
        ),
        responses={
            201: 'Classification Started',
            400: 'Bad Request - invalid form',
            404: 'Model not found'
        }
    )
    def post(self, request, format=None):
        user_query = request.data.get('query')
        model = Model.objects.filter(id=request.data.get('model', 1)).first()
        if not model:
            return Response({'status': False, 'msg': 'Model does not exist'}, status=status.HTTP_404_NOT_FOUND)
        cleaned_data = {"user_message": user_query, "target_model": model.id}
        classify_ser = Classification_request_Serializer_form(data=cleaned_data)
        if classify_ser.is_valid():
            classify = classify_ser.save()
        else:
            return Response(classify_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        classify.init_classification()
        return Response({'status': True, 'msg': 'Classification Started', 'class_id': classify.id,
                         "access_key": classify.secret_key}, status=status.HTTP_201_CREATED)

