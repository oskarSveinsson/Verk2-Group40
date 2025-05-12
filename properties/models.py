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

class FinalizedOffer(models.Model):
    id = models.BigAutoField(primary_key=True)
    offer = models.OneToOneField(PurchaseOffer, on_delete=models.CASCADE, db_column='offer_id')

    class Meta:
        managed = False
        db_table = 'finalized_offers'

class ContactInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    offer = models.OneToOneField(PurchaseOffer, on_delete=models.CASCADE, db_column='offer_id')
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'contactinfo'

class PaymentInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    offer = models.ForeignKey(PurchaseOffer, on_delete=models.CASCADE, db_column='offer_id')
    pay_method = models.CharField(max_length=13)
    card_holder = models.CharField(max_length=100, null=True, blank=True)
    card_number = models.CharField(max_length=100, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    cvc = models.CharField(max_length=4, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    mortgage_provider = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'payment_info'





