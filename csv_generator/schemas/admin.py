from django.contrib import admin

from .models import Schema, Column, DataSet


class SchemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'modified', 'column_separator', 'string_character')

class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema', 'data_type', 'order', 'isrange', 'from_range', 'to_range')

admin.site.register(Schema, SchemaAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(DataSet)
