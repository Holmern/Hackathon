# Generated by Django 4.0.3 on 2022-05-18 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(db_index=True, max_length=35)),
                ('name', models.CharField(db_index=True, max_length=35)),
            ],
        ),
    ]
