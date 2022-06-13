# Generated by Django 4.0.5 on 2022-06-10 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='from_range',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='column',
            name='isrange',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='column',
            name='to_range',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]