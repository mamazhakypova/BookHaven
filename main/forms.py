from django import forms 
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateBookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}))
    autor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите автора'}))
    year_of_manufacture = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите год выпуска'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите цену'}))
    currence = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    book_pdf = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Book
        fields = ['title', 'autor', 'year_of_manufacture', 'description', 'image', 'book_pdf', 'genre', 'price', 'currency']


class CreateCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "3", 'placeholder': 'Ваше впечатление...'}))
    class Meta:
        model = Comment
        fields = ['comment', 'review']


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте имя пользователя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите почту'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))
    class Meta: 
        model = User
        fields =['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))