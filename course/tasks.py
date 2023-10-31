from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.reverse import reverse

from config import settings
from course.models import Subscription, Course
from users.models import User


@shared_task
def sending_update(pk, url):
    letterforuser = Subscription.objects.filter(course=pk)
    course = Course.objects.get(pk=pk)
    recipients = []
    for use in letterforuser:
        email = use.user.email
        recipients.append(email)

    if recipients:
        result = send_mail(
            subject=f'Обновление курса {course.name}',
            message=f'Обновление по ссылке {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipients
        )
        print(recipients, result)
#
#
def user_active():
    today = timezone.now()
    user_apdate = User.objects.filter(last_login__lte=(today - timedelta(days=30)), is_active=True)
    print(user_apdate)
    user_apdate.update(is_active=False)
    print(user_apdate)


    #User.objects.filter(last_entrance=datetime.date.today())
