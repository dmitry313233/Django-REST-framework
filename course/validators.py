import re

from rest_framework.exceptions import ValidationError


class ValidatorUrl:
    # def __call__(self, value):
    #     reg = re.compile('https://www.youtube.com')
    #     temp_val = dict(value).get(self.field)
    #     if not bool(reg.match(temp_val)):
    #         raise ValidationError('Используем только Youtube!')

    def __call__(self, value):
        if not re.match(r'^https://www\.youtube\.com/', value):
            raise ValidationError('Запрещено использовать ссылки на ресурсы, кроме YouTube')