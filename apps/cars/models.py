from django.db import models


class CarModel(models.Model):
    class Meta:
        db_table = 'cars'

    brand = models.CharField(max_length=15)
    year = models.IntegerField()
    seats_number = models.IntegerField()
    car_body = models.CharField(max_length=15)
    engine_volume = models.FloatField()
