# Generated by Django 4.0.5 on 2022-06-10 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0003_alter_department_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]