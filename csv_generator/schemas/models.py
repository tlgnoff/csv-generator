from typing import Text
from django.db import models
from django.utils import timezone
from django.db.models import F

from users.models import User


class Schema(models.Model):

    class ColumnSeparator(models.TextChoices):
        COMMA  = ',', 'Comma (,)'
        SEMICOLON = ';', 'Semicolon (;)'


    class StringCharacter(models.TextChoices):
        SINGLE = "'", "Single-quote (')"
        DOUBLE = '"', 'Double-quote (")'


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    modified = models.DateField(default=timezone.now)
    column_separator = models.CharField(
        max_length=1,
        choices=ColumnSeparator.choices,
        default=ColumnSeparator.COMMA)
    string_character = models.CharField(
        max_length=1,
        choices=StringCharacter.choices,
        default=StringCharacter.DOUBLE)

    def __str__(self):
        return self.name


class Column(models.Model):

    class DataType(models.TextChoices):
        FULL_NAME = 'Full name'
        JOB = 'Job'
        EMAIL = 'Email'
        INTEGER = 'Integer'
        TEXT = 'Text'
        DOMAIN_NAME = 'Domain name'
        PHONE_NUMBER = 'Phone number'
        COMPANY_NAME = 'Company name'
        ADDRESS = 'Address'
        Date = 'Date'


    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=100)
    data_type = models.CharField(
        max_length=20,
        choices=DataType.choices)
    order = models.PositiveIntegerField()
    isrange = models.BooleanField(default=False)
    from_range = models.IntegerField(blank=True, null=True)
    to_range = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.data_type == self.DataType.INTEGER:
            self.isrange = True
        elif self.data_type == self.DataType.TEXT:
            self.isrange = True
        super(Column, self).save(*args, **kwargs)
            

    def __str__(self):
        return self.name


def dataset_path(instance, filename):
    return f'{instance.schema.user.id}/{instance.schema.name}/{filename}'


class DataSet(models.Model):

    class Status(models.IntegerChoices):
        READY = 0, 'Ready'
        PROCESSING = 1, 'Processing'


    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.PROCESSING)
    file = models.FileField(upload_to=dataset_path, blank=True, null=True)
