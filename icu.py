from geopy.geocoders import Nominatim
import argparse
import requests
import datetime


geolocator = Nominatim()
loginData = { 'identity' : 'ayarrab3@gmail.com',
              'password' : 'team17NETWORKAPPS' }
#d = datetime.datetime.strptime(fecha, "%Y/%m/%d")
d1 = datetime.datetime.now() + datetime.timedelta(days=15)
dstr = datetime.datetime.now().strftime("%Y-%m-%d")
d1str = d1.strftime("%Y-%m-%d")

def getLatitude(zipcode):
    location = geolocator.geocode(zipcode)
    return str(location.latitude)

def getLongitude(zipcode):
    location = geolocator.geocode(zipcode)
    return str(location.longitude)

def getTLE(satID):
    resp1 = requests.post('https://www.space-track.org/ajaxauth/login', json=loginData)
    if(resp1.status_code != 200):
        print("Login failed")
        return str(resp1.status_code)

##    resp = requests.get('https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/'
##                        +satID+"/EPOCH/"+dstr+"--"+d1str, cookies=resp1.cookies)
    resp = requests.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/'
                        +satID+"/predicates/TLE_LINE0,TLE_LINE1,TLE_LINE2", cookies=resp1.cookies)
    if(resp.status_code != 200):
        print("Response went wrong")
        return str(resp.status_code)
    getPasses(resp.json())

def getPasses(TLE):
    print(TLE[0]['TLE_LINE0'])
    print(TLE[0]['TLE_LINE1'])
    print(TLE[0]['TLE_LINE2'])

def main():
 
    parser = argparse.ArgumentParser()

    parser.add_argument('-z', required=True, dest="zipcode")
    parser.add_argument('-s', required=True, dest="satID")

    arguments = parser.parse_args()

    getTLE(arguments.satID);
    print("Latitude: " + getLatitude(arguments.zipcode))
    print("Longitude: " + getLongitude(arguments.zipcode))

if __name__ == "__main__":
    main()
