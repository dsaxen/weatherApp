from django import forms
from indesApp.models import Location
from django_countries.fields import CountryField

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

CHOICES = (('1', 'Celsius',), ('2', 'Fahrenheit'))

class WeatherForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Select city'}))
    country = CountryField()
    temperaturescale = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}), choices=CHOICES, initial='1', label="")
    class Meta:
        model = Location
        fields = ('city', 'country',)

class registerForm(UserCreationForm): #extending the usercreationform

    first_name = forms.CharField(max_length=25, required=False)
    last_name = forms.CharField(max_length=25, required=False)
    email = forms.EmailField(max_length=100, help_text="Required")

    def __init__(self, *args, **kwargs):
        super(registerForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "8+ characters"
        self.fields['password2'].help_text = ""
        self.fields['username'].help_text = "Required"
        self.fields['first_name'].help_text = "Optional"
        self.fields['last_name'].help_text = "Optional"

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
