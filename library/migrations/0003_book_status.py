# Generated by Django 3.1.7 on 2021-06-17 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_bookreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.BooleanField(default=False, help_text='Display active on site'),
        ),
    ]
