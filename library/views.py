from django.db.models.query_utils import select_related_descend
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from .models import Book, Author, BookReview
from taggit.models import Tag
from .forms import BookSearchForm
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Q 

def index(request):
    return render(request, 'index.html')

class Book_Search_View(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        search_book_list = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))
        return search_book_list

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']

    def get_success_url(self):
        return reverse_lazy('books')

class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'biography', 'date_of_birth', 'date_of_death']
    initial = {'date_of_birth': 'MM/DD/YYYY'}   
    def get_success_url(self):
        return reverse_lazy('authors')

class BookReviewCreate(LoginRequiredMixin, CreateView):
    model = BookReview
    fields = ['book', 'title', 'summary', 'review_score']


    def form_valid(self, form):
        bookReview = form.save(commit=False)
        bookReview.reviewer = self.request.user
        bookReview.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('reviews')

def book_list_view(request):
    books = Book.objects.filter(status=True)

    if request.method == 'POST':
        search_form = BookSearchForm(request.POST)

        if search_form.is_valid():
            search_term = search_form.cleaned_data['search']
            found_books = Book.objects.filter(tags__icontains=search_term)
    
    else:
        search_form = BookSearchForm()
        found_books = None


    context = {
        'book_list': books,
        'found_books': found_books,
        'form': search_form,
    }

    return render(request, 'library/book_list.html', context=context)

class AllBookListView(generic.ListView):
    model = Book
    form_class = BookSearchForm

    def get_queryset(self):
        return Book.objects.filter(status=True)

class BookInfoView(generic.DetailView):
    model = Book

def book_info_view(request, pk):

    book = get_object_or_404(Book, pk=pk)
    reviews_for_book = BookReview.objects.filter(book=book).order_by('-created_date')

    context = {
        'book': book,
        'reviews': reviews_for_book,
    }

    return render(request, 'library/book_detail.html', context=context)

class AllAuthorListView(generic.ListView):
    model = Author

class AuthorInfoView(generic.DetailView):
    model = Author

class BookReviewListView(generic.ListView):
    model = BookReview

    def get_queryset(self):
        return BookReview.objects.all().order_by('-created_date')

class BookReviewInfoView(generic.DetailView):
    model = BookReview

class LoginUserView(LoginView):
    template_name = 'registration/login.html'

def search_view(request):


    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            search_term = search_form.cleaned_data['search']
            related_books = Book.objects.get(tags__icontains=search_term)
            related_bookreviews = BookReview.objects.get(tags__icontains=search_term)
            related_author = Author.objects.get(tags__icontains=search_term)
    
    else:
        search_form = SearchForm()
        related_items = None
        related_author = None
        related_bookreviews = None
        related_books = None

    context = {
        'related_items': related_items,
        'form': search_form,
        'books': related_books,
        'authors': related_author,
        'bookreviews': related_bookreviews
    }

    return render(request, 'library/search.html', context)

