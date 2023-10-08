import datetime

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import render

from newspaper_agency.models import Topic, Newspaper


def index(request: HttpRequest):
    newspapers = Newspaper.objects.prefetch_related("publishers")
    num_topics = Topic.objects.all().count()
    total_newspapers = newspapers.all().count()
    num_last_month = newspapers.filter(
        published_date__gt=(
                datetime.date.today() - datetime.timedelta(weeks=4)
        )
    ).count()
    num_staff = get_user_model().objects.all().count()
    context = {
        "num_topics": num_topics,
        "num_last_month": num_last_month,
        "total_newspapers": total_newspapers,
        "num_staff": num_staff
    }
    return render(request, "pages/index.html", context=context)
