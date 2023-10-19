from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):   #2 задание

    class Meta:
        model = User
        fields = '__all__'
