# Generated by Django 5.1.1 on 2025-06-24 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VigilanceAPP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='telefone',
            field=models.CharField(max_length=18),
        ),
    ]
