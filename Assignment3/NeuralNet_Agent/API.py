import googlemaps
import json
from pprint import pprint
from Pawan_IndividualProject.Assignment3 import settings


class googleApi:

    def __init__(self):
        credentials = settings.joinpath(settings.CREDENTIALS, 'credentials.txt')
        # print(credentials)
        # Define API key
        self.API_KEY = None
        if settings.os.path.exists(credentials):
            with open(credentials, "r") as key:
                self.API_KEY = key.read()

    def placesSearch(self, client, searchTerm, **kwargs):
        places_result = client.places(searchTerm, **kwargs)
        # pprint(f'places result :{places_result}')
        return places_result

    def addressLookup(self, client, streetAddress):
        geocode_result = client.geocode(streetAddress)
        # pprint(f'gecode response: {geocode_result}')
        print(geocode_result[0]['geometry']['location'])
        location = geocode_result[0]['geometry']['location']
        return location['lat'], location['lng']

    def shopSearch(self, streetAddress):
        # Define client
        if self.API_KEY is not None:
            gmaps = googlemaps.Client(key=self.API_KEY)
            # streetAddress = "1234 SomeStreet St SomeCity SomeProvince F6F 6F6"
            # streetAddress = "260 Franklyn Rd Kelowna BC V1X 8C!"
            searchTerm = "computer repair store"
            latitude, longitude = self.addressLookup(gmaps, streetAddress)
            coordinates = (latitude, longitude)
            places_result = self.placesSearch(gmaps, searchTerm, location=coordinates)
            with open('placesSearch.json', 'w') as jsonFile:
                json.dump(places_result, jsonFile, indent=4, sort_keys=True)
        else:
            print("API key is not found :(")
        pass



def main():
    gsearch = googleApi()
    streetAddress = ""
    gsearch.shopSearch(streetAddress)


if __name__ == '__main__':
    main()
