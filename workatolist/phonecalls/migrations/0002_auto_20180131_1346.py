# Generated by Django 2.0.1 on 2018-01-31 13:46

from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('phonecalls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='call',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('started_at'), nulls_last=True)]},
        ),
    ]
