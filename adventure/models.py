from django.db import models

# Local imports
import math
import re

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers
    
    
    def get_distribution(self) -> list:
        # with the "standard distribution" in a vehicle, from top to bottom and left to right.
        # A Vehicle can have "n" rows with a maximum of 2 passengers per row.
        # The rows number depends on the vehicle max capacity.
        max_rows = 2
        passengers = self.passengers
        distribution = []
        for i in range(math.ceil(passengers/max_rows)):
            if i + 1 > passengers/max_rows and passengers % 2:
                distribution.append([True, False])
            else:
                distribution.append([True, True])
        return distribution
    
    @staticmethod
    def validate_number_plate(number_plate: str) -> bool:
    # a valid number plate consists of three pairs of alphanumeric chars separated by hyphen
    # the first pair must be letters and the rest must be numbers
    # e.g: AA-12-34
        return re.match(r'^[A-Za-z]{2}-[0-9]{2}-[0-9]{2}$', number_plate) is not None


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"
    
    def is_finished(self) -> bool:
        return bool(self.end)

    
