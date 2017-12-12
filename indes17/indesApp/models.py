from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model): #extending the user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=100)
    language = models.CharField(max_length=100, default="English")
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Location(models.Model): #these are stored only in case the user chooses to favorite a location
    city = models.CharField(max_length=100)
    country = CountryField(blank_label='Select country')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
