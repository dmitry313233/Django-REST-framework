from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=50, verbose_name='имя')
    phone = models.IntegerField(verbose_name='номер телефона')
    city = models.CharField(max_length=80, verbose_name='город')
    avatar = models.ImageField(upload_to='', null=True, blank=True, verbose_name='аватар')
    email = models.EmailField(unique=True, verbose_name='почта')  # все поля от обычного пользователя, но авторизацию заменить на email; Уточнить как это?

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone} {self.city}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'




