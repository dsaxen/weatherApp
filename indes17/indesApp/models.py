from django.db import models
from django_countries.fields import CountryField
# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=100)
    country = CountryField(blank_label='Select country')
    
