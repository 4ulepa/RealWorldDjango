from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class Feature(models.Model):
    title = models.CharField(max_length=250, default='', verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Свойства события'
        verbose_name_plural = 'Свойства событий'


class Category(models.Model):
    title = models.CharField(max_length=90, default='', verbose_name='Категория')

    def __str__(self):
        return self.title

    def display_event_count(self):
        pass

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Event(models.Model):
    title = models.CharField(max_length=200, default='', verbose_name='Название')
    description = models.TextField(default='', verbose_name='Описание')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    participants_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000)],
                                                           verbose_name='Количество участников')
    is_private = models.BooleanField(default=False, verbose_name='Частное')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='events')
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return f'{self.title} | Дата начала - {self.date_start}'

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Enroll(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='enrolls')
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL, related_name='enrolls')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Запись на событие'
        verbose_name_plural = 'Записи на событие'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='reviews')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Событие', related_name='reviews')
    rate = models.PositiveSmallIntegerField(verbose_name='Оценка', null=True)
    text = models.TextField(default='', verbose_name='Коментарий')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'