# Generated by Django 3.1.7 on 2021-06-15 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(help_text='Enter a review of the book', max_length=1000)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('review_score', models.CharField(blank=True, choices=[('1', '1-Star'), ('2', '2-Star'), ('3', '3-Star'), ('4', '4-Star'), ('5', '5-Star')], default='1', help_text='Given Score', max_length=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookreviewbooks', to='library.book')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookreviewusers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]
