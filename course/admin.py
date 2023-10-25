from django.contrib import admin

from course.models import Course


# Register your models here.

@admin.register(Course)
class MailingSettings(admin.ModelAdmin):
    list_display = ('name', 'description', 'id')
