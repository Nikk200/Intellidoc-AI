# Generated by Django 5.0 on 2024-09-05 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_alter_extractedtext_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='extracted_text',
        ),
    ]
