from django.conf.urls import url
from food_via_trip import views


urlpatterns = [
    url(r'^location/$', views.LocationList.as_view(), name='LocationList')
]