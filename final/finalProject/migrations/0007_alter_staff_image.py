# Generated by Django 5.0.4 on 2024-05-26 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalProject', '0006_remove_staff_image_url_staff_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.CharField(default='static/neologo.png', max_length=1000),
        ),
    ]
