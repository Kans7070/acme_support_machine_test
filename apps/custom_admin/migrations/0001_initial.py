# Generated by Django 4.0.5 on 2022-06-08 13:06

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=50)),
                ('created_by', models.CharField(max_length=50)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateField(blank=True, null=True)),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
