from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from course.models import Course, Lesson, Payment
from course.permissions import IsModerator, IsOwnerOrStaff, IsSuperuser
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]  # Это пишем для того чтобы без аунтефикации не было доступа к курсам(cource)
    # pagination_class = CoursePaginator

    def perform_create(self, serializer):  # Для сохранения владельца
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonCreateAPIView(
    generics.CreateAPIView):  # Это дженерик, спомощью дженерика мы уменьшаем количество кода по сравнению если бы мы писали в viewsets!
    serializer_class = LessonSerializer  # Отправляем данные
    permission_classes = [IsAuthenticated, ~IsModerator]  # ~ это означает not

    def perform_create(self, serializer):  # Для сохранения владельца
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    # def get_object(self, queryset=None):  # ЭТО ПИШЕСТЯ ДЛЯ ТOГО ЧТОБЫ МЕНЕДЖЕР НЕ МОГ СОЗДАВАТЬ УРОКИ
    #     self.object = super().get_object(queryset)
    #     if self.object.owner != self.request.user and not self.request.user.is_superuser:   # Это строка для менеджера
    #         raise Http404
    #     return self.object


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]  # Это пишем для того чтобы без аунтефикации не было доступа к урокам(Lesson)
    # pagination_class = CoursePaginator

    def get_queryset(self):
        """Получение объектов Lesson в зависимости от пользователя"""
        queryset = super().get_queryset()

        if self.request.user.groups.filter(name='Модератор').exists():
            return queryset.all()
        elif self.request.user:
            return queryset.filter(owner=self.request.user)
        else:
            return queryset.none()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [
        IsOwnerOrStaff | IsModerator | IsSuperuser]  # ~ это означает not


# class PaymentsCreateAPIView(generics.CreateAPIView):
#     serializer_class = PaymentsSerializer
#
#
class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'payment_method')
    ordering_fields = ('date_pay',)
#
#
# class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
#     serializer_class = PaymentsSerializer
#     queryset = Payments.objects.all()
#
#
#
#
# class PaymentsDestroyAPIView(generics.DestroyAPIView):
#     queryset = Payments.objects.all()
