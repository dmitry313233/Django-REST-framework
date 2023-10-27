from django.urls import path

from course.apps import CourseConfig

from rest_framework.routers import DefaultRouter
from course.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, subscription_setup, payment_for_course

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson/create'),
    path('lesson/list/', LessonListAPIView.as_view(), name='lesson/list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payments/list/', PaymentListAPIView.as_view(), name='Payments/list'),

    path('subscription_setup/<int:pk>/', subscription_setup, name='subscription_setup'),
    path('payment_for_course/<int:pk>/', payment_for_course, name='payment_for_course'),

] + router.urls
