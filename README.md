# saturntest
 
# Saturntest Django Application

## Overview

This application allows users to upload transcript files (.txt) and extracts financial information into three categories: Assets, Expenditures, and Income. The extracted financial information is stored in the database and can be retrieved via API endpoints.

## Features

- Upload transcript files and process them to extract financial information.
- Categorize extracted information into Assets, Expenditures, and Income.
- Retrieve the extracted financial information through an API.

## Setup Instructions

### Prerequisites

- Python 3.12.4
- Django 5.0.7
- Django Rest Framework 3.15.2

### Installation

1. **Clone the repository:**
   ```bash
   git clone 
   cd saturnappsrc
   python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
