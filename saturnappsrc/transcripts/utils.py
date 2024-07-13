import re
from .models import FinancialInfo

def process_transcript(file_path, transcript_id):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    assets_pattern = re.compile(r'(\basset\b.*?\.|\bassets\b.*?\.)', re.IGNORECASE)
    expenditures_pattern = re.compile(r'(\bexpenditure\b.*?\.|\bexpenditures\b.*?\.)', re.IGNORECASE)
    income_pattern = re.compile(r'(\bincome\b.*?\.|\bincomes\b.*?\.)', re.IGNORECASE)

    assets = assets_pattern.findall(content)
    expenditures = expenditures_pattern.findall(content)
    incomes = income_pattern.findall(content)

    if not (assets or expenditures or incomes):
        print("No financial information found.")
        return

    for fact in assets:
        FinancialInfo.objects.create(transcript_id=transcript_id, category='Assets', fact=fact)
    for fact in expenditures:
        FinancialInfo.objects.create(transcript_id=transcript_id, category='Expenditures', fact=fact)
    for fact in incomes:
        FinancialInfo.objects.create(transcript_id=transcript_id, category='Income', fact=fact)
