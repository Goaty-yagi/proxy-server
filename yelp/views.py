from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from os import getenv
import requests


class YelpApi(APIView):
    def post(self, request):
        id = request.data.get('id')
        endpoint = request.data.get('endpoint')
        
        if not id or id != settings.SECRET_KEY:
            return Response({'message': 'Invalid or missing id'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not endpoint or 'api.yelp.com' not in endpoint:
            return Response({'message': 'Invalid or missing endpoint'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            keys = getenv('YELP_API_KEY')
            if not keys:
                raise EnvironmentError("YELP_API_KEY not set in environment")
            
            keyList = keys.split(',')
            for key in keyList:
                response = requests.get(endpoint, headers={
                'Authorization': f"Bearer {key}"
                })
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    pass

            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        
        except requests.exceptions.HTTPError as http_err:
            return Response({'message': f"HTTP error: {http_err}"}, status=response.status_code)
        except requests.exceptions.RequestException as req_err:
            return Response({'message': f"Request error: {req_err}"}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as err:
            return Response({'message': f"An unexpected error occurred: {err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

