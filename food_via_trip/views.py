from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import requests
import uuid
from food_via_trip.serializers import LocationSerailizer
from food_via_trip.models import Location


# Create your views here.

class LocationList(APIView):
    def post(self, request):
        if not request.data.get('address'):
            return Response("Please provide address!", status=status.HTTP_400_BAD_REQUEST)
        address = request.data.get('address')
        # if Location.objects.filter(address = address).exists():
        #    return Response('already exist', status = status.HTTP_302_FOUND)

        locationFromAddress = settings.GLOBAL_SETTINGS['LOCATION_BASE_URI'] + '?query=' + address
        header = {"User-agent": "curl/7.43.0", "Accept": "application/json",
                  "user_key": settings.GLOBAL_SETTINGS['USER_KEY']}
        response = requests.get(locationFromAddress, headers=header)
        if not response:
            return Response("Zomoto Api didn't responding", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # not storing entire data of the response just storing useful one
        resp_json_payload = response.json()['location_suggestions'][0]
        data = {}
        data['id'] = uuid.uuid4()
        data['entity_id'] = resp_json_payload['entity_id']
        data['entity_type'] = resp_json_payload['entity_type']
        data['lat'] = resp_json_payload['latitude']
        data['long'] = resp_json_payload['longitude']
        data['address'] = address
        serializer = LocationSerailizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class PopulateRestaurantWithFare(APIView):

        def get(self, request, id):
            if not id:
                return Response("Please provide id!", status=status.HTTP_400_BAD_REQUEST)
            if not Location.objects.filter(id=id).exists():
                return Response("ID doesn't exists", status=status.HTTP_404_NOT_FOUND)
            query = Location.objects.get(id=id)
            entity_id = query.entity_id
            entity_type = query.entity_type
            start_lat = query.lat
            start_long = query.long

            restourents = settings.GLOBAL_SETTINGS['LOCATION_DETAILS_BASE_URI'] + '?entity_id=' + str(
                entity_id) + '&entity_type=' + str(entity_type)
            header = {"User-agent": "curl/7.43.0", "Accept": "application/json",
                      "user_key": settings.GLOBAL_SETTINGS['USER_KEY']}
            response = requests.get(restourents, headers=header)
            if not response:
                return Response("Zomoto Api didn't responding", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            resp_json_payload = response.json()['best_rated_restaurant']

            # fetch top 10 best rated restourant
            for restaurant in resp_json_payload:
                name = restaurant['restaurant']['name']
                end_lat = restaurant['restaurant']['location']['latitude']
                end_long = restaurant['restaurant']['location']['longitude']
                rating = restaurant['restaurant']['user_rating']['aggregate_rating']

            # print 'The coordinate for restourent ' + name.encode('utf8') + ' is ' + str(_lat )  + ' and ' + str(_lng) + ' and rating is ' + _rating.encode('utf8')
            calculateFare = settings.GLOBAL_SETTINGS[
                                'TAXI_FARE_BASE_URI'] + '?server_token=' + settings.GLOBAL_SETTINGS['SERVER_TOKEN'] + '&start_latitude=' + str(
                start_lat) + '&start_longitude=' + str(start_long) + '&end_latitude=' + str(
                end_lat) + '&end_longitude=' + str(end_long)
            response = requests.get(calculateFare)
            res_uber_json = response.json()
            prices = res_uber_json['prices']
            for price in prices:
                print price['localized_display_name'].encode('utf8') + ' and ' + str(price['low_estimate'])


















