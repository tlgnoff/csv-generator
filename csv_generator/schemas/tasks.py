import csv
import random
from celery import shared_task
from faker import Faker
from pathlib import Path
from django.conf import settings
from django.core.files.base import ContentFile
from io import StringIO

from .models import DataSet, Schema


fake = Faker()


def generate_full_name():
    return fake.name()


def generate_job():
    return fake.job()


def generate_email():
    return fake.email()


def generate_integer(from_range, to_range):
    return random.randrange(from_range, to_range)


def generate_text(from_range, to_range):
    sentences = fake.sentences(nb=random.randrange(from_range, to_range))
    return ' '.join(sentences)


def generate_domain_name():
    return fake.domain_name()


def generate_phone_number():
    return fake.phone_number()


def generate_company_name():
    return fake.company()


def generate_address():
    return fake.address()


def generate_date():
    return fake.date()


def generate_by_type(column):
    """Call data generation function based on data type."""
    if column.data_type == 'Full name':
        return generate_full_name()
    elif column.data_type == 'Job':
        return generate_job()
    elif column.data_type == 'Email':
        return generate_email()
    elif column.data_type == 'Integer':
        return generate_integer(column.from_range, column.to_range)
    elif column.data_type == 'Text':
        return generate_text(column.from_range, column.to_range)
    elif column.data_type == 'Domain name':
        return generate_domain_name()
    elif column.data_type == 'Phone number':
        return generate_phone_number()
    elif column.data_type == 'Company name':
        return generate_company_name()
    elif column.data_type == 'Address':
        return generate_address()
    elif column.data_type == 'Date':
        return generate_date()
    else:
        return 'NULL'


@shared_task
def generate_fake_data(num_rows, schema_id, dataset_id):
    """Generate CSV file with fake data."""
    schema = Schema.objects.get(id=schema_id)
    dataset = DataSet.objects.get(id=dataset_id)
    columns = schema.columns.all().order_by('order')
    path = Path(f'{schema.user.id}/{schema.name}')
    path.mkdir(parents=True, exist_ok=True)
    filename = path / f'{schema.name}_{dataset.created_date}_{dataset.id}.csv'
    csvfile = StringIO()
    writer = csv.writer(
        csvfile,    
        delimiter=schema.column_separator,
        quotechar=schema.string_character)
    writer.writerow([column.name for column in columns])
    for row in range(num_rows):
        writer.writerow([generate_by_type(column) for column in columns])
    dataset.file.save(filename.name, ContentFile(csvfile.getvalue().encode('utf-8')))
    dataset.status = DataSet.Status.READY
    dataset.save()
