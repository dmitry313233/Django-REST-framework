from django.contrib import admin

from course.models import Course, Subscription


# Register your models here.

@admin.register(Course)
class MailingSettings(admin.ModelAdmin):
    list_display = ('name', 'description', 'id')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('course', 'user',)
