from rest_framework.serializers import ModelSerializer

from apps.cars.models import CarModel


class CarsSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'year')


class CarSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'
