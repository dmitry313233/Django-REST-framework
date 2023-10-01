from rest_framework import serializers

from course.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):  # Описываем сериализатор
    # count_lesson = serializers.IntegerField(source='lessons.all.count')   # Кастомное поле    1 Метод  подсчёта уроков

    count_lesson = serializers.SerializerMethodField()   #2 Метод подсчёта уроков
    lessons = LessonSerializer(many=True)  # Заданиe 3  # Кастомное поле(дополнительное)

    class Meta:
        model = Course
        fields = ['name', 'description', 'lessons', 'count_lesson']

    def get_count_lesson(self, instance):    #2 Метод подсчёта уроков
        return instance.lessons.all().count()

    # def get_lesson(self, instance):
    #     return Lesson.get_lesson(instance)  # Заданиe 3




class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
