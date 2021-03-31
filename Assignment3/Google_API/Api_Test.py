import googlemaps
import json
import requests
import pandas as pd

from Pawan_IndividualProject.Assignment3 import settings

credentials = settings.joinpath(settings.CREDENTIALS, 'credentials.txt')
# print(credentials)


def main():
    # API_KEY = None
    # if settings.os.path.exists(credentials):
    #     with open(credentials, "r") as key:
    #         API_KEY = key.read()
    #
    # # Define client
    # if API_KEY is not None:
    #     someDict = {
    #         "address_component": '123 SomeRoad Rd'
    #     }
    #     client = googlemaps.Client(key=API_KEY)
    #
    #     somefunction(client, **someDict)
    # else:
    #     print("API key is not found")

    someDict = {
        "address_component": '123 SomeRoad Rd'
    }
    client = {"client": "dummy"}

    places_result = somefunction(client, **someDict)

    someOtherDict = {"address_component": '123 SomeRoad Rd',
                     "adr_address": "something",
                     "business_status": "something",
                     "formatted_address": "something",
                     "geometry": "something",
                     "icon": "something",
                     "name": "something",
                     "permanently_closed": False,
                     "photo": "something",
                     "place_id": "something",
                     "plus_code": "something",
                     "type": "something",
                     "url": "something",
                     "utc_offset": "+7",
                     "vicinity": "something",
                     "extraKey": "something extra"}

    try:
        places_result = somefunction(client, **someOtherDict)
    except Exception:
        print("places_result() failed")
    pass


def validPlacesFields(func):
    def places(client, **kwargs):
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
        if kwargs.keys() <= PLACES_DETAIL_FIELDS_BASIC:
            result = func(client, **kwargs)
            return result
        else:
            raise Exception(f'invalid: {kwargs.keys()} must be one of the keywords: {PLACES_DETAIL_FIELDS_BASIC}')

    return places


@validPlacesFields
def somefunction(client, **kwargs):
    places_result = None
    # places_result = client.places(client, **kwargs)

    return places_result


if __name__ == '__main__':
    main()
