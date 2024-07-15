from rest_framework import serializers
from .models import *
from django.utils import timezone

class Model_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['__all__']

class Classification_request_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Classification_request
        fields = ['__all__']

