from django.urls import path
from yelp.views import YelpApi
# from .views import ''

urlpatterns = [
    path('yelp/', YelpApi.as_view()),
]
