from rest_framework import serializers
from .models import Transcript, FinancialInfo

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['file']


class FinancialInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialInfo
        fields = ['id', 'transcript', 'category', 'fact']
