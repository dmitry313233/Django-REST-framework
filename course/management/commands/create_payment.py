import json

from django.core.management import BaseCommand

from course.models import Payment, Course
from users.models import User


class Command(BaseCommand):  # Это кастомная команда(которая будет вызываться в консоли)
    def handle(self, *args, **options):  # если * то мы можем передать любое количество неименнованных аргументов(0), если ** то мы можем передать люьое колличество именнованных аргументов(СЛОВАРЬ)
        with open('data.json', 'r', encoding='utf-8') as file:
            lst = json.load(file)

        for data in lst:
            course = data.pop('course')
            user = data.pop('user')
            object = Payment(**data)
            object.course = Course.objects.get(pk=course)
            object.user = User.objects.get(pk=user)
            object.save()


