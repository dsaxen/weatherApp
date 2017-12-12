from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import WeatherForm, registerForm
from .models import Location, Profile
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import login, logout, authenticate
from django.contrib import auth

import requests
import json

class RequestWeather(View):

    def get(self, request):
        cities = []
        form = WeatherForm()
        return render(request,'requestweather.html', {'form' : form, 'favoritelocations': cities}) #show the form

    def post(self, request):
        if 'requestweather' in request.POST: #if we click on the search button
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


                weather_url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + "," + country + "&units=" + temperaturescale + "&APPID=6adaf3b890674929a8d84b1585f05967"#The weather request
                req= requests.get(weather_url)

                if req.status_code != 200: #http not OK, the user typed in something wrong
                    messages.add_message(request, messages.INFO, 'You typed the city name wrong or chose the wrong country. Please check your spelling.')
                    return render(request,'requestweather.html', {'form' : form})

                else:
                    reqjson = req.json()

                data = reqjson
                weather = [] #list to put basic data in

                finnishdate = "Today"
                temperature = str((round(float(data["list"][0]["main"]["temp"])))) + " °" + temperatureunit

                windspeed = str((round(float(data["list"][0]["wind"]["speed"])))) + " m/s"
                winddirection = str((round(float(data["list"][0]["wind"]["deg"]))))
                cloudiness = data["list"][0]["weather"][0]["description"]

                pressure =  str((round(float(data["list"][0]["main"]["pressure"])))) + " hPa"
                humidity =  str((round(float(data["list"][0]["main"]["humidity"])))) + "%"
                verbalcloudiness = data["list"][0]["weather"][0]["description"].capitalize()
                cloudinesspercent = str(data["list"][0]["clouds"]["all"]) + "%"

                weatherday = [] #list for one day's weather
                weatherday.append(finnishdate)
                weatherday.append(temperature)
                weatherday.append(windspeed)
                weatherday.append(cloudiness)

                weatherday.append(verbalcloudiness)
                weatherday.append(pressure)
                weatherday.append(humidity)
                weatherday.append(cloudinesspercent)
                weather.append(weatherday) #weather right now

                for i in range (5, len(data["list"])): #loop through the data for future days, take the values at 3pm (usually the warmest time of the day)
                    if (data["list"][i]['dt_txt'].split(' ')[1] == "15:00:00"):

                        #BASIC INFORMATION
                        date = data["list"][i]['dt_txt']
                        year = date.split('-')[0]
                        month = date.split('-')[1]
                        day = date.split('-')[2].split(' ')[0]
                        finnishdate = day+"."+month+"."+year
                        temperature = str((round(float(data["list"][i]["main"]["temp"])))) + " °" + temperatureunit

                        windspeed = str((round(float(data["list"][i]["wind"]["speed"])))) + " m/s"
                        winddirection = str((round(float(data["list"][i]["wind"]["deg"]))))
                        cloudiness = data["list"][i]["weather"][0]["description"]

                        #EXTRA INFORMATION (WHEN YOU CLICK ON THE DATE)

                        pressure =  str((round(float(data["list"][i]["main"]["pressure"])))) + " hPa"
                        humidity =  str((round(float(data["list"][i]["main"]["humidity"])))) + "%"
                        verbalcloudiness = data["list"][i]["weather"][0]["description"].capitalize()
                        cloudinesspercent = str((round(float(data["list"][i]["clouds"]["all"])))) + "%"

                        weatherday = [] #list for one day's weather
                        weatherday.append(finnishdate)
                        weatherday.append(temperature)
                        weatherday.append(windspeed)
                        weatherday.append(cloudiness)


                        weatherday.append(verbalcloudiness)
                        weatherday.append(pressure)
                        weatherday.append(humidity)
                        weatherday.append(cloudinesspercent)

                        weather.append(weatherday)
                cities = []

                if request.user.is_authenticated:
                    locations = Location.objects.filter(profile = request.user.profile) #hide the button if you already have the city in favorites
                    for location in locations:
                        cities.append(location.city) #extracts the city names


                return render(request,'requestweather.html', {'form': form, 'weather' : weather, 'city': city, 'country': country, 'favoritelocations': cities }) #send data to template to be rendered

        elif 'addtofavorites' in request.POST: #user clicked on the add to favorites button. We process the request.

            if request.user.is_authenticated: #we ensure that the user is logged in
                city = request.POST.get('city')
                country = request.POST.get('country')
                location = Location(city=city, country=country, profile=User.objects.get(pk=request.user.id).profile)
                location.save()

                user = User.objects.get(pk=request.user.id).profile
                user.location_set.add(location) #store the favorite location

                messages.add_message(request, messages.SUCCESS, "Added " + city + " to your favorites.")

                #--------------------request the same data again-------------#

                form = WeatherForm(request.POST)
                temperaturescale = 'metric'
                temperatureunit = "C"

                weather_url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + "," + country + "&units=" + temperaturescale + "&APPID=6adaf3b890674929a8d84b1585f05967"#The weather request
                req= requests.get(weather_url)

                if req.status_code != 200: #http not OK, the user typed in something wrong
                    messages.add_message(request, messages.INFO, 'You typed the city name wrong or chose the wrong country. Please check your spelling.')
                    return render(request,'requestweather.html', {'form' : form})

                else:
                    reqjson = req.json()

                data = reqjson
                weather = [] #list to put basic data in

                finnishdate = "Today"
                temperature = str((round(float(data["list"][0]["main"]["temp"])))) + " °" + temperatureunit

                windspeed = str((round(float(data["list"][0]["wind"]["speed"])))) + " m/s"
                winddirection = str((round(float(data["list"][0]["wind"]["deg"]))))
                cloudiness = data["list"][0]["weather"][0]["description"]

                pressure =  str((round(float(data["list"][0]["main"]["pressure"])))) + " hPa"
                humidity =  str((round(float(data["list"][0]["main"]["humidity"])))) + "%"
                verbalcloudiness = data["list"][0]["weather"][0]["description"].capitalize()
                cloudinesspercent = str(data["list"][0]["clouds"]["all"]) + "%"

                weatherday = [] #list for one day's weather
                weatherday.append(finnishdate)
                weatherday.append(temperature)
                weatherday.append(windspeed)
                weatherday.append(cloudiness)

                weatherday.append(verbalcloudiness)
                weatherday.append(pressure)
                weatherday.append(humidity)
                weatherday.append(cloudinesspercent)
                weather.append(weatherday) #weather right now

                for i in range (5, len(data["list"])): #loop through the data for future days, take the values at 3pm (usually the warmest time of the day)
                    if (data["list"][i]['dt_txt'].split(' ')[1] == "15:00:00"):

                        #BASIC INFORMATION
                        date = data["list"][i]['dt_txt']
                        year = date.split('-')[0]
                        month = date.split('-')[1]
                        day = date.split('-')[2].split(' ')[0]
                        finnishdate = day+"."+month+"."+year
                        temperature = str((round(float(data["list"][i]["main"]["temp"])))) + " °" + temperatureunit

                        windspeed = str((round(float(data["list"][i]["wind"]["speed"])))) + " m/s"
                        winddirection = str((round(float(data["list"][i]["wind"]["deg"]))))
                        cloudiness = data["list"][i]["weather"][0]["description"]

                        #EXTRA INFORMATION (WHEN YOU CLICK ON THE DATE)

                        pressure =  str((round(float(data["list"][i]["main"]["pressure"])))) + " hPa"
                        humidity =  str((round(float(data["list"][i]["main"]["humidity"])))) + "%"
                        verbalcloudiness = data["list"][i]["weather"][0]["description"].capitalize()
                        cloudinesspercent = str((round(float(data["list"][i]["clouds"]["all"])))) + "%"

                        weatherday = [] #list for one day's weather
                        weatherday.append(finnishdate)
                        weatherday.append(temperature)
                        weatherday.append(windspeed)
                        weatherday.append(cloudiness)


                        weatherday.append(verbalcloudiness)
                        weatherday.append(pressure)
                        weatherday.append(humidity)
                        weatherday.append(cloudinesspercent)

                        weather.append(weatherday)

                cities = []

                if request.user.is_authenticated:
                    locations = Location.objects.filter(profile = request.user.profile) #hide the button if you already have the city in favorites
                    for location in locations:
                        cities.append(location.city) #extracts the city names


                return render(request,'requestweather.html', {'form': form, 'weather' : weather, 'city': city, 'country': country, 'favoritelocations': cities }) #send data to template to be rendered

def favorites(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            favorites = Location.objects.filter(profile = request.user.profile)

            if not favorites:
                messages.add_message(request, messages.INFO, "You do not have any favorites yet.")
                return HttpResponseRedirect(reverse("RequestWeather"))

            locations = [] #list for the favorite locations
            names = []
            for location in favorites:
                weather_url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + location.city + "," + location.country.code + "&units=metric&APPID=6adaf3b890674929a8d84b1585f05967"#The weather request
                req= requests.get(weather_url)
                if req.status_code != 200: #http not OK, the user typed in something wrong
                    messages.add_message(request, messages.INFO, 'You typed the city name wrong or chose the wrong country. Please check your spelling.')
                    return render(request,'requestweather.html', {'form' : form})

                else:
                    reqjson = req.json()

                data = reqjson
                weather = [] #list to put basic data in

                finnishdate = "Today"
                temperature = str(round(float(data["list"][0]["main"]["temp"]))) + " °C"

                windspeed = str((round(float(data["list"][0]["wind"]["speed"])))) + " m/s"
                winddirection = str((round(float(data["list"][0]["wind"]["deg"]))))
                cloudiness = data["list"][0]["weather"][0]["description"]

                pressure =  str((round(float(data["list"][0]["main"]["pressure"])))) + " hPa"
                humidity =  str((round(float(data["list"][0]["main"]["humidity"])))) + "%"
                verbalcloudiness = data["list"][0]["weather"][0]["description"].capitalize()
                cloudinesspercent = str(data["list"][0]["clouds"]["all"]) + "%"

                weatherday = [] #list for one day's weather
                weatherday.append(finnishdate)
                weatherday.append(temperature)
                weatherday.append(windspeed)
                weatherday.append(cloudiness)

                weatherday.append(verbalcloudiness)
                weatherday.append(pressure)
                weatherday.append(humidity)
                weatherday.append(cloudinesspercent)
                weather.append(weatherday) #weather right now

                for i in range (5, len(data["list"])): #loop through the data for future days, take the values at 3pm (usually the warmest time of the day)
                    if (data["list"][i]['dt_txt'].split(' ')[1] == "15:00:00"):

                        #BASIC INFORMATION
                        date = data["list"][i]['dt_txt']
                        year = date.split('-')[0]
                        month = date.split('-')[1]
                        day = date.split('-')[2].split(' ')[0]
                        finnishdate = day+"."+month+"."+year
                        temperature = str(round(float(data["list"][i]["main"]["temp"]))) + " °C"

                        windspeed = str((round(float(data["list"][i]["wind"]["speed"])))) + " m/s"
                        winddirection = str((round(float(data["list"][i]["wind"]["deg"]))))
                        cloudiness = data["list"][i]["weather"][0]["description"]

                        #EXTRA INFORMATION (WHEN YOU CLICK ON THE DATE)

                        pressure =  str((round(float(data["list"][i]["main"]["pressure"])))) + " hPa"
                        humidity =  str((round(float(data["list"][i]["main"]["humidity"])))) + "%"
                        verbalcloudiness = data["list"][i]["weather"][0]["description"].capitalize()
                        cloudinesspercent = str((round(float(data["list"][i]["clouds"]["all"])))) + "%"

                        weatherday = [] #list for one day's weather
                        weatherday.append(finnishdate)
                        weatherday.append(temperature)
                        weatherday.append(windspeed)
                        weatherday.append(cloudiness)


                        weatherday.append(verbalcloudiness)
                        weatherday.append(pressure)
                        weatherday.append(humidity)
                        weatherday.append(cloudinesspercent)

                        weather.append(weatherday)

                locations.append(weather) #add to list of locations

                names.append(location.city+", "+location.country.code)

                totaldata = zip(locations,names) #link the lists together for django templates


            return render(request, "favorites.html",{'user': request.user,  'weather': weather, 'locations': totaldata, 'loggedinuser': request.user.username,})

        else:
            messages.add_message(request, messages.INFO, "You have to be logged in to view your favorites.")
            return HttpResponseRedirect(reverse("RequestWeather"))

    elif request.method == "POST": #we decided to remove a favorite
        locationname = request.POST.get('locationname')
        city = locationname.split(',')[0]
        country = locationname.split(',')[1].strip()


        location = Location.objects.filter(city=city).filter(country=country).filter(profile=request.user.profile)
        location.delete()

        form = WeatherForm()
        messages.add_message(request, messages.INFO, "Removed " + city + " from your favorites.")
        return HttpResponseRedirect(reverse("RequestWeather"))

def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')
    else:
        messages.add_message(request, messages.INFO, "You have to be logged in to view your profile.")
        return HttpResponseRedirect(reverse("RequestWeather"))

def faq(request):
    return render(request,'faq.html')

def language(request):
    return render(request,'language.html')
def register(request):
            if request.method == 'POST':  # if you filled the form
                form = registerForm(request.POST)
                if form.is_valid():
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_pass = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_pass)
                    login(request, user)
                    messages.add_message(request, messages.INFO, "Registering success. You are logged in.")

                    return HttpResponseRedirect(reverse("RequestWeather"))

                else:
                    return render(request, "register.html", {'form': form})

            else:  # if you have not filled the form
                form = registerForm()

            return render(request, "register.html", {'form': form})

def login_view(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request,user)
                messages.add_message(request, messages.INFO, "You are logged in.")
                return HttpResponseRedirect(reverse("RequestWeather"))
            else:
                messages.add_message(request, messages.INFO, "Wrong username/password.")

        return render(request,"login.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "You have logged out")
        return HttpResponseRedirect(reverse("RequestWeather"))
    else:
        return HttpResponseRedirect(reverse("RequestWeather"))

