from .models import Incomejson
from rest_framework import serializers


class IncomeJsonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Incomejson
        fields = ['text', 'json']
