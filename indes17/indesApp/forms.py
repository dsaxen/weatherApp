from django import forms
from indesApp.models import Location
from django_countries.fields import CountryField
CHOICES = (('1', 'Celsius',), ('2', 'Fahrenheit'))

class WeatherForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'select city'}))
    country = CountryField()
    temperaturescale = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}), choices=CHOICES, initial='1', label="")
    class Meta:
        model = Location
        fields = ('city', 'country',)