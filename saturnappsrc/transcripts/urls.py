from django.urls import path
from .views import TranscriptUploadView,FinancialInfoListView

urlpatterns = [
    path('upload/', TranscriptUploadView.as_view(), name='transcript-upload'),
    path('financial-info/', FinancialInfoListView.as_view(), name='financial-info-list')

]