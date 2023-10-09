import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic

from newspaper_agency.forms import NewspaperSearchForm, TopicSearchForm
from newspaper_agency.models import Topic, Newspaper


def index(request: HttpRequest):
    newspapers = Newspaper.objects.prefetch_related("publishers")
    num_topics = Topic.objects.all().count()
    total_newspapers = newspapers.all().count()
    recent_publications = newspapers.filter(
        published_date__gt=(
                datetime.date.today() - datetime.timedelta(weeks=2)
        )
    )
    num_staff = get_user_model().objects.all().count()
    context = {
        "num_topics": num_topics,
        "recent_publications": recent_publications,
        "total_newspapers": total_newspapers,
        "num_staff": num_staff
    }
    return render(request, "newspaper_agency/index.html", context=context)


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 8
    template_name = "newspaper_agency/newspaper_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")

        context["search_form"] = NewspaperSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.prefetch_related("publishers")

        title = self.request.GET.get("title")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("title", "")

        context["search_form"] = TopicSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Topic.objects.prefetch_related("newspapers")

        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

