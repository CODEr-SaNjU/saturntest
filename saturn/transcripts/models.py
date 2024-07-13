from django.db import models

class Transcript(models.Model):
    file = models.FileField(upload_to='transcripts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class FinancialInfo(models.Model):
    TRANSCRIPT_TYPE_CHOICES = [
        ('ASSET', 'Asset'),
        ('EXPENDITURE', 'Expenditure'),
        ('INCOME', 'Income'),
    ]
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, related_name='financial_info')
    category = models.CharField(max_length=15, choices=TRANSCRIPT_TYPE_CHOICES)
    fact = models.TextField()

    def __str__(self):
        return f"{self.category}: {self.fact}"
