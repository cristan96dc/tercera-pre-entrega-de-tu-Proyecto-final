# Generated by Django 5.0 on 2024-04-01 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_comentario_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesor',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='profesor_images/'),
        ),
    ]
