from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

curr = [
    ('KGS', 'сом'),
    ('USD', '$'),
    ('RUB', '₽'),
    ('EUR', '€'),
    ('KZT', '₸')
]

class Book(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    image = models.ImageField(upload_to='images/book/%y/%m', verbose_name='Обложка книги')
    autor = models.CharField(max_length=200, verbose_name='Автор')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name='Жанр')
    description = models.TextField(max_length=600, verbose_name='Описание')
    year_of_manufacture = models.CharField(max_length=50, verbose_name='Год выпуска')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(max_length=10, choices=curr, null=True, blank=True, verbose_name='Валюта')
    book_pdf = models.FileField(upload_to='file/book/%y/%m', verbose_name='Книга электронная')
    is_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Genre(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

rating = [
    (1, 'Ужасно'),
    (2, 'Плохо'),
    (3, 'Нормально'),
    (4, 'Хорошо'),
    (5, 'Отлично')
]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    comment = models.TextField(max_length=350, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)], choices=rating, verbose_name='Оценка')

    def __str__(self):
        return f'Коммент от - {self.user.username}'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'