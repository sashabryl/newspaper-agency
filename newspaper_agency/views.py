import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from newspaper_agency.forms import NewspaperSearchForm, TopicSearchForm, NewspaperForm, RedactorSearchForm
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
        context["num_found"] = self.get_queryset().count()
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
        name = self.request.GET.get("name", "")
        context["num_found"] = self.get_queryset().count()
        context["search_form"] = TopicSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Topic.objects.prefetch_related("newspapers")

        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


def create_update_topic(request: HttpRequest):
    data = request.POST
    if not data.get("name_update"):
        Topic.objects.create(name=request.POST.get("name_create"))
    else:
        topic = Topic.objects.get(id=data.get("topic_id"))
        topic.name = data.get("name_update")
        topic.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")
    template_name = "newspaper_agency/newspaper_form.html"


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "newspaper_agency/newspaper_form.html"
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:newspaper-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["num_found"] = self.get_queryset().count()
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.prefetch_related("newspapers")

        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "newspaper_agency/redactor_form.html"
    success_url = reverse_lazy("newspaper_agency:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "newspaper_agency:redactor_form.html"

    def get_success_url(self):
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("agency:redactor=list")
