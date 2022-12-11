from rest_framework.serializers import ModelSerializer

from .models import CarModel


class CarSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        exclude = ('auto_park',)


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('photo',)
