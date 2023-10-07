from django.contrib import admin
from django.urls import path, include

from newspaper_agency.views import index

urlpatterns = [
    path("", index, name="index")
]

app_name = "agency"
