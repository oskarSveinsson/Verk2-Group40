from django.contrib.auth.models import User
from django.db import models

class Property(models.Model):
    id = models.IntegerField(primary_key=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    house_number = models.CharField(max_length=5)
    postal_code = models.IntegerField()
    listing_price = models.IntegerField()
    property_type = models.CharField(max_length=10)
    property_status = models.CharField(max_length=10)
    seller = models.ForeignKey(User, related_name='seller', on_delete=models.CASCADE)
    rooms = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    total_area = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.street

    class Meta:
        managed = False
        db_table = 'properties'

class PropertyImage(models.Model):
    id = models.IntegerField(primary_key=True)
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"Image for {self.property.street}"

    class Meta:
        managed = False
        db_table = 'images'
        ordering = ['id']

