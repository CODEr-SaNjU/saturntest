from django.test import TestCase
from rest_framework.test import APIClient
from .models import FinancialInfo, Transcript
from .utils import process_transcript
import os

class FinancialInfoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'test_transcript.txt')
        with open(self.test_file_path, 'w') as file:
            file.write("This is a test file with some income, assets, and expenditures.")

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_upload_transcript(self):
        with open(self.test_file_path, 'rb') as file:
            response = self.client.post('/api/upload/', {'file': file}, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Transcript.objects.exists())

    def test_financial_info_extraction(self):
        transcript = Transcript.objects.create(file=self.test_file_path)
        process_transcript(transcript.file.path, transcript.id)
        self.assertTrue(FinancialInfo.objects.filter(category='Income').exists())
        self.assertTrue(FinancialInfo.objects.filter(category='Assets').exists())
        self.assertTrue(FinancialInfo.objects.filter(category='Expenditures').exists())
