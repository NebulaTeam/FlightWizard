import pyowm
from datetime import datetime, timedelta
from geopy.distance import vincenty
from airport import Airport
import re
import urllib2

API_KEY = 'd8b93f15f524c3ea2e9f3a5379646e1e'
COMMERCIAL_AIRPLANE_SPEED = 500 # mph
TIME_FOR_TAKING_OFF_AND_LANDING = 0.5 # hour

class WeatherGrapper:
	def __init__(self, src, dest, departure_time):
		self._owm = pyowm.OWM(API_KEY)
		self._src = Airport(src)
		self._dest = Airport(dest)
		self._dep_hour, self._dep_minute = departure_time.split(":")
		distance_btn_src_dst = vincenty(self._src.lat_lng(), self._dest.lat_lng()).miles
		self._approx_duration = distance_btn_src_dst/COMMERCIAL_AIRPLANE_SPEED + TIME_FOR_TAKING_OFF_AND_LANDING

	def src_weather(self):
		forecast = self._owm.daily_forecast(self._src.location())
		t = datetime.today()
		wanted_time = datetime(t.year, t.month, t.day, int(self._dep_hour), int(self._dep_minute))
		return (forecast.get_weather_at(wanted_time), grab_visibility(self._src.icao()))

	def dest_weather(self):
		forecast = self._owm.daily_forecast(self._dest.location())
		t = datetime.today()
		wanted_time = datetime(t.year, t.month, t.day, int(self._dep_hour), int(self._dep_minute)) + timedelta(hours=self._approx_duration)
		return (forecast.get_weather_at(wanted_time), grab_visibility(self._dest.icao()))

def grab_visibility(icao):
	f = urllib2.urlopen("http://www.aviationweather.gov/taf/data?ids=" + icao + "&format=raw&metars=on&layout=off&type=json")
	html = f.read()
	match = re.search('\s[0-9]+SM\s', html)
	return float(match.group(0).strip()[0:-2])
