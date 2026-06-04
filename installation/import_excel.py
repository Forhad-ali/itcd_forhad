import os
import sys
import django
import pandas as pd
from dateutil import parser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forhad.settings')

django.setup()

from installation.models import Installation


# Excel file
file_path = os.path.join(BASE_DIR, 'data.xlsx')

# Read excel
df = pd.read_excel(file_path)


# Clean text
def clean_text(value):

    if pd.isna(value):
        return ''

    return str(value).strip()


# Universal date converter
def convert_date(value):

    if pd.isna(value):
        return None

    try:

        # Excel serial date
        if isinstance(value, (int, float)):

            if value > 1000:
                return pd.to_datetime(
                    value,
                    unit='D',
                    origin='1899-12-30'
                ).date()

        # Convert text formats
        value = str(value).strip()

        # Auto parse almost everything
        return parser.parse(
            value,
            dayfirst=True
        ).date()

    except:
        return None


count = 0

for index, row in df.iterrows():

    try:

        Installation.objects.create(

            ms_id_full=clean_text(row.get('MS ID Full')),

            ms_id=clean_text(row.get('MS_ID')),

            status=clean_text(row.get('Status')),

            abd_number=clean_text(row.get('ABD Number')),

            start_date=convert_date(row.get('Start Date')),

            end_date=convert_date(row.get('End Date')),

            system=clean_text(row.get('System')),

            facility=clean_text(row.get('Facility')),

            saw_program=clean_text(row.get('SAW Program')),

            unit=clean_text(row.get('Unit')),

            stage=clean_text(row.get('Stage'))

        )

        count += 1

        print(f"Imported Row {index + 1}")

    except Exception as e:

        print(f"Error Row {index + 1}: {e}")

print(f"\\nImport Completed: {count} rows inserted")