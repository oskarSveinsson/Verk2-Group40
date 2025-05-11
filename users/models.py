from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='seller_profile')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    seller_type = models.CharField(max_length=11)
    logo_url = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=5)
    country = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        managed = False
        db_table = 'sellers'