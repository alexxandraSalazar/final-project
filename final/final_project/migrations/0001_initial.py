# Generated by Django 5.0.4 on 2024-04-14 23:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numPC', models.IntegerField()),
                ('numLapTop', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=50)),
                ('id_staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=10)),
                ('fingerprint', models.CharField(max_length=50)),
                ('class_group', models.CharField(max_length=2)),
                ('password', models.CharField(max_length=50)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='final_project.cycle')),
                ('id_stu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation', models.CharField(max_length=244)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_feedbacks', to='final_project.staff')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='final_project.student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.TimeField(auto_now_add=True)),
                ('check_out', models.TimeField(auto_now_add=True)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='final_project.cycle')),
                ('pc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='final_project.pc')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='final_project.student')),
            ],
        ),
        migrations.CreateModel(
            name='StuFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation', models.CharField(max_length=244)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stu_feedbacks', to='final_project.staff')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='final_project.student')),
            ],
        ),
    ]