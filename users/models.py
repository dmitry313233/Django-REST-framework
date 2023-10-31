from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='имя')
    phone = models.IntegerField(null=True, blank=True, verbose_name='номер телефона')
    city = models.CharField(null=True, blank=True, max_length=80, verbose_name='город')
    avatar = models.ImageField(upload_to='', null=True, blank=True, verbose_name='аватар')
    email = models.EmailField(unique=True, verbose_name='почта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} {self.name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'




