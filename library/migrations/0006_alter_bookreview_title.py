# Generated by Django 3.2.4 on 2021-06-22 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_bookreview_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='title',
            field=models.CharField(default='', max_length=150),
        ),
    ]
