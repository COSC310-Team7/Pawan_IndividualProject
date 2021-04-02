import googlemaps
import json
from pprint import pprint
from Pawan_IndividualProject.Assignment3 import settings


# TODO: change the import path as it is slightly different on Windows as MAC OS

def main(streetAddress):
    credentials = settings.joinpath(settings.CREDENTIALS, 'credentials.txt')
    # print(credentials)

    # Define API key
    API_KEY = None
    if settings.os.path.exists(credentials):
        with open(credentials, "r") as key:
            API_KEY = key.read()

    # Define client
    if API_KEY is not None:
        gmaps = googlemaps.Client(key=API_KEY)
        # streetAddress = "1234 SomeStreet St SomeCity SomeProvince F6F 6F6"
        # streetAddress = "260 Franklyn Rd Kelowna BC V1X 8C!"
        searchTerm = "computer repair store"
        latitude, longitude = addressLookup(gmaps, streetAddress)
        coordinates = (latitude, longitude)
        places_result = placesSearch(gmaps, searchTerm, location=coordinates)
        with open('placesSearch.json', 'w') as jsonFile:
            json.dump(places_result, jsonFile, indent=4, sort_keys=True)
    else:
        print("API key is not found :(")
    pass


# Test function to parse the saved JSON retrieved by placesSearch
def searchResults():
    path = settings.joinpath(settings.GOOGLE_API_PATH, 'placesSearch.json')
    with open(path) as jsonFile:
        searchedLocations = json.load(jsonFile)
    for businesses in searchedLocations["results"]:
        name = businesses["name"]
        address = businesses["formatted_address"]
        rating = businesses["rating"]
        print("---- ", name, " ----")
        print("Address: ", address)
        print("Rating: ", rating)
        print()


def test():
    someFields = ["address_component"]
    client = {"client": "dummy"}
    searchTerm = "computer repair store"
    places_result = placesSearch(client, fields=someFields)
    print(places_result)

    someOtherFields = ["address_component",
                       "adr_address",
                       "business_status",
                       "formatted_address",
                       "geometry",
                       "icon",
                       "name",
                       "permanently_closed",
                       "photo",
                       "place_id",
                       "plus_code",
                       "type",
                       "url",
                       "utc_offset",
                       "vicinity",
                       "extraKey"
                       ]

    try:
        places_result = placesSearch(client, fields=someOtherFields)
    except Exception:
        print("places_result() failed")
    pass


def validPlacesFields(func):
    def places(*args, **kwargs):
        PLACES_DETAIL_FIELDS_BASIC = {"address_component",
                                      "adr_address",
                                      "business_status",
                                      "formatted_address",
                                      "geometry",
                                      "icon",
                                      "name",
                                      "permanently_closed",
                                      "photo",
                                      "place_id",
                                      "plus_code",
                                      "type",
                                      "url",
                                      "utc_offset",
                                      "vicinity", }

        if 'fields' in kwargs:
            if set(kwargs['fields']) <= PLACES_DETAIL_FIELDS_BASIC:
                result = func(*args, **kwargs)
                return result
            else:
                raise Exception(f'invalid: {kwargs.keys()} must be one of the keywords: {PLACES_DETAIL_FIELDS_BASIC}')
        else:
            result = func(*args, **kwargs)
            return result

    return places


@validPlacesFields
def placesSearch(client, searchTerm, **kwargs):
    places_result = client.places(searchTerm, **kwargs)
    pprint(f'places result :{places_result}')
    return places_result


def addressLookup(client, streetAddress):
    geocode_result = client.geocode(streetAddress)
    pprint(f'gecode response: {geocode_result}')
    # print(geocode_result[0]['geometry']['location'])
    location = geocode_result[0]['geometry']['location']
    return location['lat'], location['lng']


if __name__ == '__main__':
    # test()
    # main()
    searchResults()
