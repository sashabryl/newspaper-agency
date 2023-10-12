from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper_agency.models import Topic, Newspaper


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
        url = reverse("agency:topic-create-update")
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_protection_delete(self):
        url = reverse("agency:topic-delete", args=[1])
        res = self.client.get(url)
        self.assertNotEquals(res.status_code, 200)


class TestCreateUpdateTopic(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="tester", password="29fjaeoiwf@")
        self.topic = Topic.objects.create(name="Art")
        self.client.force_login(self.user)

    def test_create_update_topic_works_all_right(self):
        url = reverse("agency:topic-create-update")
        self.client.post(url, data={"name_create": "Tourism"})
        self.assertTrue(Topic.objects.filter(name="Tourism").exists())
        self.client.post(
            url, data={
                "name_update": "Love",
                "topic_id": 1,
            }
        )
        self.assertTrue(Topic.objects.filter(name="Love").exists())
