from geopy.geocoders import Nominatim
from twilio.rest import TwilioRestClient
import pygame
import argparse
import requests
import datetime


#sms sound and gpio
def sendSMS(body):
        account_sid = "AC0d11dcf9eeea54fc1a42de65006d44e3"
        auth_token = "f360c891f7d9fc2f783bc98c65819cba"
        client = TwilioRestClient(account_sid, auth_token)

        message = client.messages.create(to="+18048366909", from_="+12604680505",
                                             body="Hello there!")
        return

def playSound():
        pygame.mixer.init()
        pygame.mixer.music.load("radio.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
                continue
        return

def checkTime(time):
	now = datetime.now()
	if((now - time) <= timedelta(minutes = 15)):
		return True
	else:
		return False


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
