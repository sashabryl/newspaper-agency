from django.contrib import admin
from django.urls import path, include

from newspaper_agency.views import index, NewspaperListView, TopicListView

urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("topics/", TopicListView.as_view(), name="topic-list")
]

app_name = "agency"
