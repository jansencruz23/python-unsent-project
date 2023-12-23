# Generated by Django 4.2.8 on 2023-12-23 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='letter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='website.letter'),
            preserve_default=False,
        ),
    ]