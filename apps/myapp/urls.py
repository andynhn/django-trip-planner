from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^travels$', views.travels),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^travels/destination/(?P<tripid>\d+)$', views.show),
    url(r'^travels/destination/join/(?P<tripid>\d+)$', views.join),
    url(r'^travels/add$', views.add),
    url(r'^travels/add_trip$', views.add_trip),
    url(r'^logout$', views.logout),
]