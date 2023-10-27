from rest_framework import serializers

from course.models import Course, Lesson, Payment, Subscription
from course.services import conver_currensies

from course.validators import ValidatorUrl


class LessonSerializer(serializers.ModelSerializer): # Это сериалайзер. Этот сериалайзер описывает то что я буду видеть в Postman
    url = serializers.URLField(validators=[ValidatorUrl()], required=False)  # required=False это позволяет пренебречь этим полем

    class Meta:
        model = Lesson
        fields = '__all__'



class CourseSerializer(serializers.ModelSerializer):  # Описываем сериализатор
    count_lesson = serializers.SerializerMethodField()   #2 Метод подсчёта уроков
    lessons = LessonSerializer(many=True, read_only=True)  # Заданиe 3  # Кастомное поле(дополнительное)  Тоесть переменная lessons равна всем значениям LessonSerializer
    usd_price = serializers.SerializerMethodField()  # !!!!!!!

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lessons', 'count_lesson', 'usd_price', 'amount']

    def get_usd_price(self, instance):   # !!!!!
        return conver_currensies(instance.amount, instance.name)  # Возвращаем метод в services, instance.amount обращаемся к Course.amount

    def get_count_lesson(self, instance):    #2 Метод подсчёта уроков
        return instance.lessons.all().count()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('course', 'user')
