# Generated by Django 4.2.2 on 2023-09-29 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('random_contacts_app', '0002_myuser_delete_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='linkedin_token',
        ),
    ]
