from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import FinancialFact
import io

class TranscriptUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('transcript-upload')

    def test_upload_empty_file(self):
        with io.StringIO("") as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'The file is empty.')

    def test_upload_non_utf8_file(self):
        with io.BytesIO(b'\x80\x81\x82') as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'File encoding not supported. Please upload a UTF-8 encoded file.')

    def test_upload_file_with_no_financial_info(self):
        content = "This is a transcript with no financial information."
        with io.StringIO(content) as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No financial information found in the transcript.')

    def test_upload_valid_file(self):
        content = "Mr. Thompson's salary is Â£15,000. He has Â£200,000 in savings."
        with io.StringIO(content) as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('assets', response.data)
        self.assertIn('income', response.data)

    def test_database_entry_creation(self):
        content = "Mr. Thompson's salary is Â£15,000. He has Â£200,000 in savings."
        with io.StringIO(content) as file:
            self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(FinancialFact.objects.count(), 2)
        self.assertEqual(FinancialFact.objects.filter(category='income').count(), 1)
        self.assertEqual(FinancialFact.objects.filter(category='asset').count(), 1)
