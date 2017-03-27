import argparse
import requests
import datetime
import sys
import math
import ephem
import json

loginData = { 'identity' : 'ayarrab3@gmail.com',
              'password' : 'team17NETWORKAPPS' }
googleAPIkey_elevation = 'AIzaSyDcehBBYBrtHGlGdJ8zTj0JaXj2kqo78Jo'
googleAPIkey_geocoding = 'AIzaSyB8WgEbB-mOGI1bcq2AficBiLjMJJFMLJs'
#d = datetime.datetime.strptime(fecha, "%Y/%m/%d")
d1 = datetime.datetime.now() + datetime.timedelta(days=14)
dstr = datetime.datetime.now().strftime("%Y-%m-%d")
d1str = d1.strftime("%Y-%m-%d")

def getCoordinates(zipcode):
    resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+zipcode+'&key='+googleAPIkey_geocoding)
    if(resp.status_code != 200):
        print("Response went wrong")
        return str(resp.status_code)
    latitude = resp.json()['results'][0]['geometry']['location']['lat']
    longitude = resp.json()['results'][0]['geometry']['location']['lng']
    return (str(latitude),str(longitude))

def getElevation(latitude, longitude):
    
    resp = requests.get('https://maps.googleapis.com/maps/api/elevation/json?locations='+latitude+','+longitude+
                         '&key='+googleAPIkey_elevation)
    if(resp.status_code != 200):
        print("Response went wrong")
        return str(resp.status_code)
    return(resp.json()['results'][0]['elevation'])
    
def getTLE(satID):
    resp1 = requests.post('https://www.space-track.org/ajaxauth/login', json=loginData)
    
    if(resp1.status_code != 200):
        print("Login failed")
        return str(resp1.status_code)

    resp = requests.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/'
                        +satID+"/predicates/TLE_LINE0,TLE_LINE1,TLE_LINE2", cookies=resp1.cookies)
    
    if(resp.status_code != 200):
        print("Response went wrong")
        return str(resp.status_code)
    
    return (resp.json())

def datetime_from_time(tr):
    year, month, day, hour, minute, second = tr.tuple()
    dt = datetime.datetime(year, month, day, hour, minute, int(second))
    return dt

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
        print ((datetime.datetime.now() + datetime.timedelta(day)).strftime("%m-%d-%Y"), i['weather'][0]['description'])
        day = day+1;
    return cal

def getPasses(TLE, latitude, longitude, elevation, weather):
    print(TLE[0]['TLE_LINE0'])
    print(TLE[0]['TLE_LINE1'])
    print(TLE[0]['TLE_LINE2'])

    iss = ephem.readtle(TLE[0]['TLE_LINE0'], TLE[0]['TLE_LINE1'], TLE[0]['TLE_LINE2'])

    obs = ephem.Observer()
    obs.lat = latitude
    obs.long = longitude
    obs.elevation = elevation
    obs.pressure = 0
    obs.horizon = '-0:34'

    now = datetime.datetime.now()
    obs.date = now

    tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
    
    while (ephem.localtime(tr) < d1 ):
        
##        print("""Date/Time (UTC)       Alt/Azim	  Lat/Long	Elev""")
##        print("""=====================================================""")
##        while tr < ts:
##            obs.date = tr
##            iss.compute(obs)
##            print ("%s | %4.1f %5.1f | %4.1f %+6.1f | %5.1f" % 
##                        (tr, 
##			 math.degrees(iss.alt), 
##			 math.degrees(iss.az), 
##			 math.degrees(iss.sublat), 
##			 math.degrees(iss.sublong), 
##			 iss.elevation/1000.))
##            tr = ephem.Date(tr + 20.0 * ephem.second)
        duration = int((ts - tr) *60*60*24)
        rise_time = datetime_from_time(tr)
        max_time = datetime_from_time(tt)
        set_time = datetime_from_time(ts)

        obs.date = max_time

        sun = ephem.Sun()
        sun.compute(obs)
        iss.compute(obs)

        sun_alt = math.degrees(sun.alt)
        visible = False
        if (iss.eclipsed is False and -18 < math.degrees(sun_alt) < -6):
            visible = True

        max_time_date = max_time.strftime("%m-%d-%Y")
##        print(max_time_date)
##        print(max_time)

##        if((weather[max_time_date] == ['sky is clear']) & visible ):
        if (visible):
            print(max_time_date)
                  
        obs.date = tr + ephem.minute
        tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
        #print(d1)

def getVisiblePasses(satID, latitude, longitude, elevation, weather):

    TLE = getTLE(satID)
    getPasses(TLE, latitude, longitude, elevation, weather)
    
def main():
 
    parser = argparse.ArgumentParser()

    parser.add_argument('-z', required=True, dest="zipcode")
    parser.add_argument('-s', required=True, dest="satID")

    arguments = parser.parse_args()

    weatherCond = getNOAA(arguments.zipcode)
    (latitude,longitude) = getCoordinates(arguments.zipcode)
    print("Latitude: " + latitude + "    Longitude: " + longitude)
    
    elevation = getElevation(latitude, longitude)
    
    getVisiblePasses(arguments.satID, latitude, longitude, elevation, weatherCond)

    print(elevation)

if __name__ == "__main__":
    main()
