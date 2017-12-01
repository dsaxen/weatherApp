from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import WeatherForm
from .models import Location

import requests
import json

class RequestWeather(View):
    def get(self, request):
        form = WeatherForm() 
        return render(request,'requestweather.html', {'form' : form}) #show the form
    
    def post(self, request):
        
        form = WeatherForm(request.POST)
        if form.is_valid(): 
            cd = form.cleaned_data
            
            city = cd['city'].capitalize()
            country = cd['country']
            temperaturescale = cd['temperaturescale']

            if (temperaturescale == "1"): #radiobuttons
                temperaturescale = 'metric'
                temperatureunit = "C"
            else:
                temperaturescale = 'imperial'
                temperatureunit = "F"
                
            location = Location(city=city,country=country)
            location.save()
            
            weather_url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + "," + country + "&units=" + temperaturescale + "&APPID=6adaf3b890674929a8d84b1585f05967"#The weather request
            req= requests.get(weather_url)
                
            if req.status_code != 200: #http not OK, the user typed in something wrong
                reqjson = 'N/A'
                return render(request,'requestweather.html', {'form' : form})
            else:
                reqjson = req.json()    
            data = reqjson
            print(data)
            
            weather = [] #list to put basic data in
            
            finnishdate = "Today"
            temperature = str((round(float(data["list"][0]["main"]["temp"])))) + " °" + temperatureunit
            
            windspeed = str((round(float(data["list"][0]["wind"]["speed"])))) + " m/s"
            winddirection = str((round(float(data["list"][0]["wind"]["deg"]))))
            cloudiness = data["list"][0]["weather"][0]["description"]
            
            
            
            
            weatherday = [] #list for one day's weather
            weatherday.append(finnishdate)
            weatherday.append(temperature)
            weatherday.append(windspeed)
            weatherday.append(cloudiness)
            weather.append(weatherday) #weather right now
            
            for i in range (5, len(data["list"])): #loop through the data for future days, take the values at 3pm (usually the warmest time of the day)
                if (data["list"][i]['dt_txt'].split(' ')[1] == "15:00:00"):
                    date = data["list"][i]['dt_txt']    
                    year = date.split('-')[0]
                    month = date.split('-')[1]
                    day = date.split('-')[2].split(' ')[0]
                    finnishdate = day+"."+month+"."+year 
                    temperature = str((round(float(data["list"][i]["main"]["temp"])))) + " °" + temperatureunit
            
                    windspeed = str((round(float(data["list"][i]["wind"]["speed"])))) + " m/s"
                    winddirection = str((round(float(data["list"][i]["wind"]["deg"]))))
                    cloudiness = data["list"][i]["weather"][0]["description"]
            
                    weatherday = [] #list for one day's weather
                    weatherday.append(finnishdate)
                    weatherday.append (temperature)
                    weatherday.append (windspeed)
                    weatherday.append (cloudiness)
                    weather.append(weatherday) #weather right now
                    
            return render(request,'requestweather.html', {'form': form, 'weather' : weather, 'city': city, 'country': country}) #send data to template to be rendered
            
def favorites(request):
    return render(request,'favorites.html')

def profile(request):
    return render(request,'profile.html')

def faq(request):
    return render(request,'faq.html')

def language(request):
    return render(request,'language.html')
def register(request):
    return render(request,'register.html')
def login(request):
    return render(request,'login.html')
            
            
            
            
            
            