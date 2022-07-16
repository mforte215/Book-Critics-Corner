from django.contrib import admin

# Register your models here.
from .models import Genre, Book, Language, Author, BookReview

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', 'biography', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

class GenreAdmin(admin.ModelAdmin):
    pass

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'status')

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'title', 'book', 'review_score')


class LangaugeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Language, LangaugeAdmin)
admin.site.register(BookReview, BookReviewAdmin)