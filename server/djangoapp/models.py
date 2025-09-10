from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class CarModel(models.Model):
    TYPE_CHOICES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="SUV")
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)],
    )

    def __str__(self) -> str:
        return self.name
