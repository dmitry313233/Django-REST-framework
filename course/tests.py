import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            name='django',
            city='USA',
            email='django_sky@mail.ru'
        )

        self.course = Course.objects.create(
            name='test',
            description='test',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name='test',
            description='test',
            course=self.course,
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):  # Тестируем создание урока
        data = {'name': 'new_test', 'description': 'test', 'course': self.lesson.pk, 'owner': self.lesson.pk}
        response = self.client.post(
            reverse('course:lesson/create'), data=data    # Это путь в url
        )

        #print(response.json())


        self.assertEqual(  # Это сравнение статуса нашего кода со статусом этой ошибки HTTP_201_CREATED
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(   # Это сравнение с получаемыми данными
            response.json(),
            {'avatar': None,
             'course': 1,
             'description': 'test',
             'id': 2,
             'name': 'new_test',
             'owner': 1,
             'url': None}

        )

        self.assertTrue(
            Course.objects.all().exists()   # Здесь пишем курс так как у нас путь прописан
        )

    def test_lesson_list(self):   # Тестируем список уроков

        response = self.client.get(
            reverse('course:lesson/list')
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'], [{'id': self.lesson.pk, 'url': None, 'name': 'test', 'description': 'test', 'avatar': None, 'course': self.course.pk, 'owner': self.user.pk}]

        )

        self.assertTrue(
            Course.objects.all().exists()
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse('course:lesson_get', args=[self.lesson.pk])
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_lesson_update(self):

        update_data = {'id': self.lesson.pk, 'name': 'new_test', 'description': 'test', 'course': self.course.pk, 'owner': self.user.pk}
        response = self.client.put(
            reverse('course:lesson_update', args=[self.lesson.pk]),
            data=update_data
        )

        #print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        #print(Course.objects.filter(pk=self.lesson.pk).first())

        self.assertEqual(
            response.json()['name'], 'new_test'
        )
        self.assertFalse(
            Course.objects.filter(pk=self.lesson.pk).exists()
        )

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse('course:lesson_delete', args=[self.lesson.pk]),
        )

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            name='django',
            city='USA',
            email='django_sky@mail.ru'
        )

        self.course = Course.objects.create(
            name='test',
            description='test',
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)  # Эта строка выполняет аунтификацию пользователя указанного в аргументе user

    def test_subscription_setup(self):
        response = self.client.get(
            reverse('course:subscription_setup', args=[self.course.pk])
        )
        #print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(), {'Success': 'Вы подписались'}
        )

        response = self.client.get(
            reverse('course:subscription_setup', args=[self.course.pk])
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        #print(response.json())

        self.assertEqual(
            response.json(), {'Message': 'Вы отписались от курса'}
        )

        self.assertTrue(
            Course.objects.filter(pk=self.course.pk).exists())
