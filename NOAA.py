import requests
import json
import datetime

def getNOAA(zipcode):
	zipVal = str(zipcode)
	APIVal = "1eb667941c31e677adf539ed22c7adcd"

	NOAA = 'http://api.openweathermap.org/data/2.5/forecast/daily?zip='+zipVal+'&cnt=15&APPID='+APIVal

	NOAAresp = requests.get(NOAA)
	result = NOAAresp.json()

	day = 0
	cal = {}

	for i in result['list']:
		cal [(datetime.datetime.now() + datetime.timedelta(day)).strftime("%m-%d-%Y")] = i['weather'][0]['description']
		print (datetime.datetime.now() + datetime.timedelta(day)).strftime("%m-%d-%Y"), i['weather'][0]['description']
		day = day+1;


##getNOAA(24060)