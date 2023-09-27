from django.db import models

# Create your models here.

class Course(models.Model):  # Или models.Model  9# Это задание 3
    name = models.CharField(max_length=70, verbose_name='название')
    avatar = models.ImageField(upload_to='', null=True, blank=True, verbose_name='аватар')
    discription = models.TextField(max_length=150, null=True, blank=True, verbose_name='описание')

    def __str__(self):
        return f'{self.name} {self.discription}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):  # 11 Это задание 3
    name = models.CharField(max_length=70, verbose_name='название')
    discription = models.TextField(max_length=150, null=True, blank=True, verbose_name='описание')
    avatar = models.ImageField(upload_to='', null=True, blank=True, verbose_name='аватар')
    url = models.URLField(max_length=30, unique=True, null=True, blank=True, verbose_name='Email')

    def __str__(self):
        return f'{self.name} {self.url}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
