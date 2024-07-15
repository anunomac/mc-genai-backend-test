from rest_framework import serializers
from .models import *
from django.utils import timezone

class Model_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"

class Model_Serializer_Public(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ["id","public_name"]

class Classification_request_Serializer(serializers.ModelSerializer):
    target_model= Model_Serializer_Public()
    class Meta:
        model = Classification_request
        exclude=["secret_key"]
        # fields = "__all__"

class Classification_request_Serializer_form(serializers.ModelSerializer):
    # target_model= Model_Serializer_Public()
    class Meta:
        model = Classification_request
        exclude=["secret_key"]
        # fields = "__all__"
