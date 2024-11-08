# Generated by Django 4.2.8 on 2023-12-23 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_letter_delete_record'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.CharField(max_length=12)),
                ('message', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=200)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]
