from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import CharField
from django.urls import reverse
import uuid;
from django.shortcuts import get_object_or_404
from django.db.models.functions import Coalesce
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Fantasy)')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', related_name='books', on_delete=SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a short description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                             help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False, help_text='Display active on site')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-info', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())

    display_genre.short_description = 'Genre'

    def rating_avg(self):
        return BookReview.objects.filter(book=self).aggregate(
            avg=Coalesce(models.Avg('review_score'),0, output_field=CharField()),)['avg']

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(max_length=2000, help_text="Enter a short description of the author")
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-info', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the original language the book was written in.")

    def __str__(self):
        return self.name

class BookReview(models.Model):
    title = models.CharField(max_length=150, default='', blank=False)
    reviewer = models.ForeignKey(User, on_delete=CASCADE, related_name='bookreviewusers')
    book = models.ForeignKey(Book, on_delete=CASCADE, related_name='bookreviewbooks')
    summary = RichTextField()
    created_date = models.DateField(auto_now_add=True, editable=False)
    tags = TaggableManager()

    REVIEW_STARS = (
        ('1', '1-Star'),
        ('2', '2-Star'),
        ('3', '3-Star'),
        ('4', '4-Star'),
        ('5', '5-Star'),
    )

    review_score = models.CharField(
        max_length=1,
        choices=REVIEW_STARS,
        blank=True,
        default='1',
        help_text='Given Score',
    )

    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f'{self.book.title} by {self.reviewer.username}'

    def get_absolute_url(self):
        return reverse('review-info', args=[str(self.id)])
    
class Post(models.Model):
    title = models.CharField(max_length=150, default='', blank=False)
    poster = models.ForeignKey(User, on_delete=CASCADE, related_name='postuser')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()