# Generated by Django 5.0 on 2024-09-01 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractedtext',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
