# Generated by Django 5.1.5 on 2025-02-15 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('id_number', models.CharField(max_length=100, unique=True)),
                ('subjects', models.TextField()),
                ('experience', models.IntegerField()),
                ('teacher_image', models.ImageField(blank=True, null=True, upload_to='teacher_images/')),
                ('teacher_bio', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(max_length=100)),
                ('date_registered', models.DateTimeField(auto_now_add=True)),
                ('teacher_approved_status', models.IntegerField(default=0)),
            ],
        ),
    ]
