# Generated by Django 4.2.2 on 2024-10-22 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_document_status_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]
