import imp
from django import forms
from django.forms import BaseModelFormSet, HiddenInput, modelformset_factory

from .models import Schema, Column


class SchemaForm(forms.ModelForm):
    
    class Meta:
        model = Schema
        fields = [
            'name',
            'column_separator',
            'string_character',
        ]


class BaseColumnFormset(BaseModelFormSet):
    deletion_widget = HiddenInput


ColumnFormset = modelformset_factory(
    Column,
    fields=('name', 'data_type', 'from_range', 'to_range', 'order'),
    formset=BaseColumnFormset,
    extra=1,
    labels={
        'name': 'Column name',
        'data_type': 'Type',
        'from_range': 'From',
        'to_range': 'To'
    },
    can_delete=True)


ColumnEditFormset = modelformset_factory(
    Column,
    fields=('name', 'data_type', 'from_range', 'to_range', 'order'),
    formset=BaseColumnFormset,
    extra=0,
    labels={
        'name': 'Column name',
        'data_type': 'Type',
        'from_range': 'From',
        'to_range': 'To'
    },
    can_delete=True)