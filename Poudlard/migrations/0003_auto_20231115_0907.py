# Generated by Django 2.2.28 on 2023-11-15 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Poudlard', '0002_auto_20231114_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='etat',
            field=models.CharField(max_length=50),
        ),
    ]
