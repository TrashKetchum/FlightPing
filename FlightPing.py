import geopy.distance
from geographiclib.geodesic import Geodesic
import requests
import math
from FlightRadar24.api import FlightRadar24API

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_longlat():
    ip = get_ip()
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()
    return (response.get("latitude"), response.get("longitude"))

def get_country():
    ip = get_ip()
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()
    return response.get("country_name").lower()

# def get_bearing(lat1, lat2, long1, long2):
#     brng = round(Geodesic.WGS84.Inverse(lat1, long1, lat2, long2)['azi1'])
#     return brng

radius = 20
myCord = get_longlat()
country = get_country()
if(country=="ireland" or country=="united kingdom"): country = "uk"
fr_api = FlightRadar24API()
zones  = fr_api.get_zones()
bounds = fr_api.get_bounds(zones['europe']['subzones'][country]) #sucks if you're not in europe but Im lazy
flights = fr_api.get_flights(bounds = bounds)



for flight in flights:
    distance = geopy.distance.geodesic(myCord,(flight.latitude, flight.longitude)).km
    if(distance<radius):
            org = flight.origin_airport_iata
            dest = flight.destination_airport_iata
            if(dest!='N/A'):
                org = fr_api.get_airport(org)['name']
                dest = fr_api.get_airport(dest)['name']
            print("PLANE ALERT \n DISTANCE: {0}km, HEADING: {1}, CALLSIGN: {2}, AIRCAFT: {3}, ORIGIN: {4}, DESTINATION {5}".format(
            math.floor(distance),
            round(flight.heading),
            flight.callsign, 
            flight.aircraft_code, 
            org,
            dest
        ))