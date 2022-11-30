from django.db import models
import datetime

from apps.auto_parks.models import AutoParkModel
from django.core import validators as V

date = datetime.date.today()


class CarModel(models.Model):
    class Meta:
        db_table = 'cars'

    brand = models.CharField(max_length=15, unique=True, validators=[
        V.MinLengthValidator(3), V.MaxLengthValidator(15)
    ])
    year = models.IntegerField(validators=[
        V.MinValueValidator(1990), V.MaxValueValidator(int(date.year))
    ])
    seats = models.IntegerField(validators=[
        V.MinValueValidator(2), V.MaxValueValidator(10)
    ])
    body = models.CharField(max_length=25, validators=[
        V.MinLengthValidator(2), V.MaxLengthValidator(15)
    ])
    engine_volume = models.FloatField(validators=[
        V.MinValueValidator(1), V.MaxValueValidator(4)
    ])
    auto_park = models.ForeignKey(AutoParkModel, on_delete=models.CASCADE, related_name='cars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
