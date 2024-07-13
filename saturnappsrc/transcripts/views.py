from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TranscriptSerializer,FinancialInfoSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import FinancialInfo
from .utils import process_transcript
from rest_framework import generics


class TranscriptUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            transcript = serializer.save()
            process_transcript(transcript.file.path, transcript.id)
            return Response({
                "message": "File uploaded successfully",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Invalid input",
            "errors": serializer.errors
        }, status=400)



class FinancialInfoListView(generics.ListAPIView):
    queryset = FinancialInfo.objects.all()
    serializer_class = FinancialInfoSerializer