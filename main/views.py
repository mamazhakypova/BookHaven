from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator


def apply_search(request, queryset):
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(title__icontains=search_query)
    return queryset, search_query


def home(request):
    books_qs = Book.objects.filter(is_active=True)
    books_qs, search_query = apply_search(request, books_qs)
    paginator = Paginator(books_qs, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'genres': Genre.objects.all(),
        'search_query': search_query
    }
    return render(request=request, template_name='index.html', context=context)

def book_view(request, id):
    book = get_object_or_404(Book, id=id)
    comments = Comment.objects.filter(book=book)
    context={'book': book, 'comments': comments}

    if request.user.is_authenticated:
        user_comment = Comment.objects.filter(book=book, user=request.user).exists()
        context['user_comment']= user_comment 

    if comments.exists():
        review = [i.review for i in comments]
        review = sum(review)/len(review)
    else:
        review = 0
    context['review'] = review
    

    if request.method == 'POST':
        form_comment = CreateCommentForm(request.POST)

        if form_comment.is_valid():
            comment = form_comment.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
            return redirect(reverse('book_view', args=[id]))
        else:
            print(form_comment.errors)

    form_comment = CreateCommentForm()
    context['form_comment'] = form_comment
    context['genres'] = Genre.objects.all()
    return render(request=request, template_name='book.html', context=context)

def add_book(request):
    genres = Genre.objects.all()

    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    form = CreateBookForm()

    if request.method == 'POST':
        form = CreateBookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('my_books')
        else:
            print(form.errors)
    return render(request=request, template_name='add_book.html', context={'form': form, 'create': True, 'genres': genres})

def validate_password_custom(password):
    try:
        validate_password(password)
    except ValidationError as e:
        return e

def login_view(request):
    form = LoginForm()
    context={'form': form}
    context['genres'] = Genre.objects.all()

    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)
            return redirect(reverse('home'))
        else:
            print(form.errors)
            context['error'] = "Неправильный логин или пароль"
    return render(request=request, template_name='login.html', context=context)

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    form = RegisterForm()
   
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Пользователь с таким именем уже существует')
            elif password1 != password2:
                form.add_error(None, 'Пароли не совпадают')
            else:
                user = form.save(commit=False)
                user.set_password(password1)
                user.save()
                login(request, user)
                return redirect('home')
    else:
        form = RegisterForm()
    context = {'form': form, 'genres': Genre.objects.all()}
    return render(request=request, template_name='register.html', context=context)

def logout_view(request):
    logout(request=request)
    return redirect(reverse('home'))

def my_books(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(is_active=True, user=request.user)
        books, search_query = apply_search(request, books)
        paginator = Paginator(books, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={'books': books, 'search_query': search_query, 'search_action': request.path, 'page_obj': page_obj}
    else:
        return redirect(reverse('login'))
    
    context['genres'] = Genre.objects.all()
    return render(request=request, template_name='my_books.html', context=context)

def view_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    books = Book.objects.filter(is_active=True, genre=genre)
    genres = Genre.objects.all()
    books, search_query = apply_search(request, books)
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request=request, template_name='genre.html', context={'genre_name': genre, 'page_obj': page_obj, 'genres': genres, 'search_query': search_query, 'search_action': request.path})

def edit_book(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('home'))
    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        form = CreateBookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            form.save()
            return redirect(reverse('book_view', args=[id]))
        else:
            print(form.errors)
    else:
        form = CreateBookForm(instance=book)
    genres = Genre.objects.all()
    return render(request=request, template_name='add_book.html', context={'form': form, 'create': False, 'genres': genres})

def delete_book(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('home'))
    book = get_object_or_404(Book, id=id)
    book.is_active = False
    book.save()
    return redirect(reverse('home'))

def genres_overview(request):
    genres = Genre.objects.all()
    genres_with_books = []
    for genre in genres:
        books = Book.objects.filter(genre=genre, is_active=True)

        if books.exists():
            genres_with_books.append({'genre': genre, 'books': books})
    return render(request=request, template_name='genres.html', context={'genres_with_books': genres_with_books, 'genres': genres})
