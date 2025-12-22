from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('book_view/<int:id>', book_view, name='book_view'),
    path('login', login_view, name='login'),
    path('register', register, name='register'),
    path('logout', logout_view, name='logout'),
    path('add_book', add_book, name='add_book'),
    path('my_books', my_books, name='my_books'),
    path('edit_book/<int:id>', edit_book, name='edit_book'),
    path('delete_book/<int:id>', delete_book, name='delete_book'),
    path('view_genre/<int:id>', view_genre, name='view_genre'),
    path('genres/', genres_overview, name='genres_overview')
]