from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from os import getenv
import requests


class YelpApi(APIView):
    def post(self, request):
        id = request.data.get('id')
        endpoint = request.data.get('endpoint')
        if id == settings.SECRET_KEY:
            if 'api.yelp.com' in endpoint:
                try:
                    key = "Bearer " + getenv('YELP_API_KEY')
                    response = requests.get(endpoint, headers= {
                        'Authorization':key
                    })
                    response.raise_for_status()
                    data = response.json()
                    return Response(data)
                
                except requests.exceptions.RequestException as e:
                    return Response(f"An error occurred: {e}", status=500)
            else:
                return Response({'message': 'endpoint is not valid'}, 400)
        else:
            return Response({'message': 'id is not correct'}, 400)

    
