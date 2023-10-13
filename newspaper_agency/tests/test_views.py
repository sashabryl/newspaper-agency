from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper_agency.forms import (
    NewspaperSearchForm,
    RedactorSearchForm,
    TopicSearchForm
)
from newspaper_agency.models import Topic, Newspaper

PAGINATION = 8
TOPIC_LIST_URL = reverse("agency:topic-list")
NEWSPAPER_LIST_URL = reverse("agency:newspaper-list")
REDACTOR_LIST_URL = reverse("agency:redactor-list")


class PublicNewspaperViewsTest(TestCase):
    def setUp(self) -> None:
        self.newspaper = Newspaper.objects.create(
            title="newzpaper", content="contend"
        )

    def test_login_required_protection_list(self):
        url = reverse("agency:newspaper-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_detail(self):
        url = reverse("agency:newspaper-detail", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_update(self):
        url = reverse("agency:newspaper-update", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_delete(self):
        url = reverse("agency:newspaper-delete", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)


class PrivateNewspaperViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="tester", password="j39fawuifh@!"
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="Art")
        for i in range(10):
            Newspaper.objects.create(title=f"abcd{i}", content="some")

        Newspaper.objects.create(title="dif1", content="some")
        Newspaper.objects.create(title="dif2", content="some")

    def test_list_searchbar_exists(self):
        url = NEWSPAPER_LIST_URL
        res = self.client.get(url)
        self.assertTrue(
            isinstance(res.context.get("search_form"), NewspaperSearchForm)
        )

    def test_list_search_bar_works(self):
        url = NEWSPAPER_LIST_URL
        form = NewspaperSearchForm(data={"title": "dif"})
        res = self.client.get(url, form.data)
        self.assertTrue(form.is_valid())
        self.assertEquals(
            list(res.context.get("newspaper_list")),
            list(Newspaper.
                 objects.filter(title__icontains="dif")[:PAGINATION]),
        )
        self.assertEquals(
            res.context.get("search_form").initial.get("title"), "dif"
        )

    def test_list_pagination_does_not_break_search(self):
        url = NEWSPAPER_LIST_URL
        res = self.client.get(url, data={"title": "abc", "page": 2})
        self.assertEquals(
            list(res.context.get("newspaper_list")),
            list(Newspaper.objects.
                 filter(title__icontains="abc")[PAGINATION:]),
        )


class PublicRedactorViewsTest(TestCase):
    def setUp(self) -> None:
        self.redactor = get_user_model().objects.create(
            username="luckyman", password="feiawfh#!@32"
        )

    def test_login_required_protection_list(self):
        url = reverse("agency:redactor-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_detail(self):
        url = reverse("agency:redactor-detail", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_update(self):
        url = reverse("agency:redactor-update", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_delete(self):
        url = reverse("agency:redactor-delete", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)


class PrivateRedactorViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="tester", password="iun2i3ulrh@!"
        )
        self.client.force_login(self.user)
        for i in range(10):
            get_user_model().objects.create(
                username=f"{i}willingcitizen", password="feiuaw!@fewa31"
            )
        get_user_model().objects.create(
            username="notwilling", password="rj329@!feia"
        )
        get_user_model().objects.create(
            username="notwilly2", password="fewa4@!2fgre"
        )

    def test_list_searchbar_exists(self):
        url = REDACTOR_LIST_URL
        res = self.client.get(url)
        self.assertTrue(
            isinstance(res.context.get("search_form"), RedactorSearchForm)
        )

    def test_list_search_bar_works(self):
        url = REDACTOR_LIST_URL
        form = RedactorSearchForm(data={"username": "not"})
        res = self.client.get(url, form.data)
        self.assertTrue(form.is_valid())
        self.assertEquals(
            list(res.context.get("redactor_list")),
            list(get_user_model().
                 objects.filter(username__icontains="not")[:PAGINATION]),
        )
        self.assertEquals(
            res.context.get("search_form").initial.get("username"), "not"
        )

    def test_list_pagination_does_not_break_search(self):
        url = REDACTOR_LIST_URL
        res = self.client.get(url, data={"username": "citizen", "page": 2})
        self.assertEquals(
            list(res.context.get("redactor_list")),
            list(get_user_model().
                 objects.filter(username__icontains="citizen")[PAGINATION:]),
        )


class PublicTopicViewsTest(TestCase):
    def setUp(self) -> None:
        self.topic = Topic.objects.create(name="Art")

    def test_login_required_protection_list(self):
        url = reverse("agency:topic-list")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_detail(self):
        url = reverse("agency:topic-detail", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_update(self):
        url = reverse("agency:topic-update", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_delete(self):
        url = reverse("agency:topic-delete", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)


class PrivateTopicViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="tester", password="feajiu@!iure43"
        )
        self.client.force_login(self.user)
        for i in range(10):
            Topic.objects.create(name=f"{i}pillow")
        Topic.objects.create(name="brick1")
        Topic.objects.create(name="brick2")

    def test_list_searchbar_exists(self):
        url = TOPIC_LIST_URL
        res = self.client.get(url)
        self.assertTrue(
            isinstance(res.context.get("search_form"), TopicSearchForm)
        )

    def test_list_search_bar_works(self):
        url = TOPIC_LIST_URL
        form = TopicSearchForm(data={"name": "brick"})
        res = self.client.get(url, form.data)
        self.assertTrue(form.is_valid())
        self.assertEquals(
            list(res.context.get("topic_list")),
            list(Topic.
                 objects.filter(name__icontains="brick")[:PAGINATION]),
        )
        self.assertEquals(
            res.context.get("search_form").initial.get("name"), "brick"
        )

    def test_list_pagination_does_not_break_search(self):
        url = TOPIC_LIST_URL
        res = self.client.get(url, data={"name": "pill", "page": 2})
        self.assertEquals(
            list(res.context.get("topic_list")),
            list(Topic.
                 objects.filter(name__icontains="pill")[PAGINATION:]),
        )
