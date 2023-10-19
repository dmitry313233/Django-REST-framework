# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from course.models import Lesson, Course
#
#
# class LessonTestCase(APITestCase):
#     def setUp(self):
#         pass
#
#     def test_create_lesson(self):  # Тестируем создание урока
#         data = {
#             'name': 'name',
#             'description': 'description'
#         }
#         response = self.client.post(
#             '/course/', data=data    # Это путь в url
#         )
#
#         self.assertEqual(  # Это сравнение статуса нашего кода со статусом этой ошибки HTTP_201_CREATED
#             response.status_code, status.HTTP_201_CREATED
#         )
#
#         self.assertEqual(   # Это сравнение с получаемыми данными
#             response.json(), {'name': 'name', 'description': 'description', 'lessons': [], 'count_lesson': 0}
#         )
#
#         self.assertTrue(
#             Course.objects.all().exists()   # Здесь пишем курс так как у нас путь прописан
#         )
#
#     def test_lesson_list(self):   # Тестируем список уроков
#         response = self.client.get(
#             '/course/'
#         )
#
#         self.assertEqual(
#             response.status_code, status.HTTP_200_OK
#         )
#
#         self.assertEqual(
#             response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []}
#         )
#
#         self.assertTrue(
#             Course.objects.all().exists()
#         )
#
#     def test_lesson_retrieve(self):
#         response = self.client.get(
#             '/course/', kwargs={'pk': self.client.pk}  # не работает рк!
#         )
#
#         self.assertEqual(
#             response.status_code, status.HTTP_200_OK
#         )
#
#     def test_lesson_update(self):
#
#         response = self.client.put(
#             '/course/', kwargs={'pk': self.client.pk}  # не работает рк!
#         )
#
#
#         self.assertEqual(
#             response.status_code, status.HTTP_200_OK
#         )
#
#         self.assertFalse(
#             Course.objects.filter(pk=self.client.pk).exists()
#         )
#
#     def test_lesson_delete(self):
#         response = self.client.delete(
#             '/course/', kwargs={'pk': self.client.pk}  # не работает рк!
#         )
#
#         self.assertEqual(
#             response.status_code, status.HTTP_204_NO_CONTENT
#         )
#
#
# class SubscriptionTestCase(APITestCase):
#     def setUp(self):
#         pass
#
#