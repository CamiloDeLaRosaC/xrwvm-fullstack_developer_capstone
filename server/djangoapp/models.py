"""Database models for vehicle makes and models."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CarMake(models.Model):
    """A vehicle manufacturer."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """A model produced by a vehicle manufacturer."""

    TYPES = [(name, name) for name in ("Sedan", "SUV", "Wagon", "Coupe", "Hatchback")]
    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="models",
    )
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=20, choices=TYPES)
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2026)]
    )

    class Meta:
        unique_together = ("car_make", "name", "year")

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
