# Generated by Django 5.0.6 on 2024-06-03 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_delete_alumno_delete_profesor_alter_proyecto_alumno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='alumno',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='profesor',
            field=models.CharField(max_length=100),
        ),
    ]
