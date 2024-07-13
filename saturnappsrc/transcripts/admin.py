from django.contrib import admin

from .models import FinancialInfo,Transcript

# Register your models here.

admin.site.register(FinancialInfo)
admin.site.register(Transcript)