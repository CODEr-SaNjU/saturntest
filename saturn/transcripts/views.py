from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TranscriptSerializer
from .models import FinancialInfo
import re

class TranscriptUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                return Response({'error': 'File encoding not supported. Please upload a UTF-8 encoded file.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the file is empty
            if not content.strip():
                return Response({'error': 'The file is empty.'}, status=status.HTTP_400_BAD_REQUEST)

            # Extract financial information
            assets = re.findall(r'\b(?:property|savings|pension|investments)\b.*?\d+.*?[\.\d+]*', content, re.IGNORECASE)
            expenditures = re.findall(r'\b(?:expenses|costs|fees|mortgage|loan)\b.*?\d+.*?[\.\d+]*', content, re.IGNORECASE)
            income = re.findall(r'\b(?:income|salary|rental income)\b.*?\d+.*?[\.\d+]*', content, re.IGNORECASE)

            # Check if no financial information was found
            if not assets and not expenditures and not income:
                return Response({'error': 'No financial information found in the transcript.'}, status=status.HTTP_400_BAD_REQUEST)

            # Save extracted data to the database
            for fact in assets:
                FinancialInfo.objects.create(category='asset', fact=fact)
            for fact in expenditures:
                FinancialInfo.objects.create(category='expenditure', fact=fact)
            for fact in income:
                FinancialInfo.objects.create(category='income', fact=fact)

            return Response({
                'assets': assets,
                'expenditures': expenditures,
                'income': income
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
