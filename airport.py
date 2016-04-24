import json
import urllib2
class Airport:
	def __init__(self, icao):
		self._data = {}
		json_data = json.load(urllib2.urlopen('http://www.airport-data.com/api/ap_info.json?icao=' + icao))
		self._data['icao'] = icao
		self._data['name'] = str(json_data['name'])
		self._data['country'] = str(json_data['country'])
		self._data['country_code'] = str(json_data['country_code'])
		self._data['location'] = str(json_data['location']).split(",")[0]
		self._data['lng'] = str(json_data['longitude'])
		self._data['lat'] = str(json_data['latitude'])

	def location(self):
		return self._data['location'] + "," + self._data['country_code']

	def lat_lng(self):
		return (self._data['lat'], self._data['lng'])

	def icao(self):
		return self._data['icao']