from django.contrib.auth.models import User
from django.db import models
from django import forms
from users.models import Seller


class Property(models.Model):
    id = models.IntegerField(primary_key=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    house_number = models.CharField(max_length=5)
    postal_code = models.IntegerField()
    listing_price = models.IntegerField()
    property_type = models.CharField(max_length=10)
    property_status = models.CharField(max_length=10)
    seller = models.ForeignKey(Seller, related_name='properties', on_delete=models.CASCADE)
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

class PurchaseOffer(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    offer_amount = models.IntegerField()
    expiration_date = models.DateField()
    submitted = models.DateField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.buyer} - {self.property}"

    class Meta:
        db_table = 'purchase_offers'
        managed = False

