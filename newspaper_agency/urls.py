from django.urls import path

from newspaper_agency.views import (
    index,
    NewspaperListView,
    TopicListView,
    NewspaperUpdateView,
    NewspaperCreateView,
    create_update_topic, NewspaperDeleteView, TopicDeleteView, RedactorDeleteView, RedactorUpdateView,
    RedactorCreateView, RedactorListView, RedactorDetailView, NewspaperDetailView, TopicDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path(
        "newspapers/<int:pk>/update/",
        NewspaperUpdateView.as_view(),
        name="newspaper-update"
    ),
    path(
        "newspapers/create/",
        NewspaperCreateView.as_view(),
        name="newspaper-create"
    ),
    path(
        "topics/create-update/",
        create_update_topic,
        name="topic-create-update"
    ),
    path(
        "newspapers/<int:pk>/delete/",
        NewspaperDeleteView.as_view(),
        name="newspaper-delete"
    ),
    path(
        "topics/<int:pk>/delete/",
        TopicDeleteView.as_view(),
        name="topic-delete"
    ),
    path(
        "redactors/",
        RedactorListView.as_view(),
        name="redactor-list"
    ),
    path(
        "redactors/create/",
        RedactorCreateView.as_view(),
        name="redactor-create"
    ),
    path(
        "redactors/<int:pk>/delete/",
        RedactorDeleteView.as_view(),
        name="redactor-delete"
    ),
    path(
        "redactors/<int:pk>/update/",
        RedactorUpdateView.as_view(),
        name="redactor-update"
    ),
    path(
        "redactors/<int:pk>/",
        RedactorDetailView.as_view(),
        name="redactor-detail"
    ),
    path(
        "newspapers/<int:pk>/",
        NewspaperDetailView.as_view(),
        name="newspaper-detail"
    ),
    path(
        "topics/<int:pk>/",
        TopicDetailView.as_view(),
        name="topic-detail"
    )
]

app_name = "agency"
