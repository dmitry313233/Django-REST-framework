# import re
#
# from rest_framework.exceptions import ValidationError
#
#
# class Validatot_url:
#     def __init__(self, field):
#         self.field = field
#
#     def __call__(self, value):
#         reg = re.compile('https://www.youtube.com')
#         temp_val = dict(value).get(self.field)
#         if not bool(reg.match(temp_val)):
#             raise ValidationError('Используем только Youtube!')
