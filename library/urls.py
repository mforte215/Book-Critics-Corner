from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list_view, name='books'),
    path('book/<int:pk>', views.book_info_view, name='book-info'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('authors/', views.AllAuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorInfoView.as_view(), name='author-info'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('reviews/', views.BookReviewListView.as_view(), name='reviews'),
    path('review/<int:pk>', views.BookReviewInfoView.as_view(), name='review-info'),
    path('review/create/', views.BookReviewCreate.as_view(), name='review-create'),
    path('book/results/', views.Book_Search_View.as_view(), name='book-search')
    
]