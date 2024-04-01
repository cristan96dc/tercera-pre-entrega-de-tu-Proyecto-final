# Generated by Django 5.0.2 on 2024-03-26 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alumno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.alumno')),
            ],
        ),
    ]
