# Generated by Django 5.0.4 on 2024-04-27 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('finalProject', '0002_alter_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', null=True, related_name='finalProject_users', related_query_name='finalProject_user', to='auth.group', verbose_name='groups'),
        ),
    ]
