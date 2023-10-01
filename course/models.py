from django.db import models

from users.models import User


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=70, verbose_name='название')
    avatar = models.ImageField(upload_to='', null=True, blank=True, verbose_name='аватар')
    description = models.TextField(max_length=150, null=True, blank=True, verbose_name='описание')

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=70, verbose_name='название')
    description = models.TextField(max_length=150, null=True, blank=True, verbose_name='описание')
    avatar = models.ImageField(upload_to='', null=True, blank=True, verbose_name='аватар')
    url = models.URLField(max_length=30, unique=True, null=True, blank=True, verbose_name='Email')

    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='урок', related_name='lessons')  # related_name это прописывается для обращения из модели на которую ссылается это поле!

    def __str__(self):
        return f'{self.name} {self.url}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):   # новая домашка

    METHOD = (
        ('наличные', 'наличные'),
        ('перевод на счет', 'перевод на счет'),
    )

    date_pay = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    summa = models.PositiveIntegerField(default=0, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=15, choices=METHOD, verbose_name='способ оплаты: наличные или перевод на счет')

    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='урок')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.user} {self.date_pay} {self.summa} {self.payment_method}'

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'
