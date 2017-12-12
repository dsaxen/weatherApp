from indesApp.views import *
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RequestWeather.as_view(), name="RequestWeather"),
    url(r'^favorites$', favorites),
    url(r'^profile$', profile),
    url(r'^faq$', faq),
    url(r'^language$', language),
    url(r'^register$', register),
    url(r'^login$', login_view),
    url(r'^logout$', logout_view),
]
