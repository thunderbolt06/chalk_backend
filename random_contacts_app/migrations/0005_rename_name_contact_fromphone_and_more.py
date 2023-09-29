# Generated by Django 4.2.2 on 2023-09-29 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('random_contacts_app', '0004_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='name',
            new_name='fromPhone',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='phone',
            new_name='toPhone',
        ),
        migrations.AddField(
            model_name='contact',
            name='dist',
            field=models.IntegerField(default=0),
        ),
    ]
