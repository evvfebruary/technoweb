# Generated by Django 2.1.1 on 2018-11-24 16:38

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('ask_evv', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='question',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
