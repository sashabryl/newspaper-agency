# Generated by Django 4.2.6 on 2023-10-13 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newspaper_agency', '0002_alter_redactor_years_of_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
