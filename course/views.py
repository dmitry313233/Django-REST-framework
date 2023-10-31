from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.reverse import reverse

from course.models import Course, Lesson, Payment, Subscription
from course.paginators import CoursePaginator
from course.permissions import IsModerator, IsOwnerOrStaff, IsSuperuser
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from course.services import conver_currensies
from course.tasks import sending_update

class CourseViewSet(viewsets.ModelViewSet):
    """View set для курса"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]  # Это пишем для того чтобы без аунтефикации не было доступа к курсам(cource)
    pagination_class = CoursePaginator

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     sending_update.delay(instance.pk, request)
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return serializer.data
        #return super().update(request, *args, **kwargs)


    def perform_update(self, serializer):  # Для отправки писем об обновлении курса  !!!!!!!
        serializer.save()
        instance = self.get_object()
        url = self.request.build_absolute_uri(reverse('course:course-detail', kwargs={'pk': instance.pk}))
        sending_update.delay(instance.pk, url)
        print('Сообщение отправлено')
        #sending_update.delay(new_subscription)

    def perform_create(self, serializer):  # Для сохранения владельца
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonCreateAPIView(generics.CreateAPIView):  # Это дженерик, спомощью дженерика мы уменьшаем количество кода по сравнению если бы мы писали в viewsets!
    """Создание для урока"""
    serializer_class = LessonSerializer  # Отправляем данные
    permission_classes = [IsAuthenticated, ~IsModerator]  # ~ это означает not  Было IsAuthenticated!!!

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
    """Список уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]  # Это пишем для того чтобы без аунтефикации не было доступа к урокам(Lesson)
    pagination_class = CoursePaginator

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
    """Детали урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Редактирование для урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление для урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff | IsModerator | IsSuperuser]  # ~ это означает not


# class PaymentsCreateAPIView(generics.CreateAPIView):
#     serializer_class = PaymentsSerializer
#
#
class PaymentListAPIView(generics.ListAPIView):
    """Список платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'payment_method')
    ordering_fields = ('date_pay',)


@api_view(['GET'])
def subscription_setup(request, pk):
    """Контроллер для осуществления подписки на курс"""
    try:
        course = Course.objects.get(pk=pk)  # В переменную course добавляем  конкретный курс, который указал пользователь в виде рк
    except Course.DoesNotExist:
        return Response({'Error': "Курса не существует"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if Subscription.objects.filter(course=course, user=request.user).exists():
            Subscription.objects.filter(course=course, user=request.user).delete()
            return Response({"Message": "Вы отписались от курса"}, status=status.HTTP_200_OK)
        data = {'course': pk, 'user': request.user.id}
        serializer = SubscriptionSerializer(data=data)
        if serializer.is_valid():  # is_valid означает действует
            serializer.save()
            return Response({'Success': "Вы подписались"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def payment_for_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
        price_link = conver_currensies(course.amount, course.name)
    except Course.DoesNotExist:
        return Response({'Error': "Курса не существует"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'price_link': price_link})

