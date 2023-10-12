from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from newspaper_agency.forms import (
    TopicSearchForm,
    NewspaperSearchForm,
    RedactorSearchForm,
    NewspaperForm,
)
from newspaper_agency.models import Topic, Newspaper


class NewspaperFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="freaoiewj",
            password="feoiaw408#f",
            years_of_experience=14,
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="Art")
        self.redactor = get_user_model().objects.create(
            username="fre42iewj",
            password="fe@w408#f",
            years_of_experience=34,
        )

    def test_publishers_topics_field_config(self):
        form = NewspaperForm()
        self.assertIn(
            "forms.widgets.CheckboxSelectMultiple object",
            str(form.fields.get("publishers").widget),
        )
        self.assertIn(
            "forms.widgets.CheckboxSelectMultiple object",
            str(form.fields.get("topics").widget),
        )

    def test_create_form_works(self):
        form = NewspaperForm(
            data={
                "title": "test_paper",
                "topics": [
                    1,
                ],
                "publishers": [
                    1,
                ],
                "content": "some",
            }
        )
        self.assertTrue(form.is_valid())
        self.client.post(reverse("agency:newspaper-create"), form.data)
        self.assertTrue(Newspaper.objects.filter(title="test_paper").exists())

    def test_update_form_works(self):
        newspaper = Newspaper.objects.create(title="new", content="cont")
        form = NewspaperForm(
            data={
                "title": "updated_paper",
                "topics": [
                    1,
                ],
                "publishers": [
                    1,
                    2,
                ],
                "content": "some",
            }
        )
        self.assertTrue(form.is_valid())
        self.client.post(
            reverse("agency:newspaper-update", args=[newspaper.id]), form.data
        )

        self.assertTrue(
            Newspaper.objects.filter(title="updated_paper").exists()
        )


class SearchFormsTest(TestCase):
    def test_topic_searchform_config(self):
        form = TopicSearchForm(data={"name": "a"})
        self.assertTrue(form.is_valid())
        self.assertIn(
            "forms.widgets.TextInput object",
            str(form.fields.get("name").widget),
        )

    def test_redactor_searchform_config(self):
        form = RedactorSearchForm(data={"username": "a"})
        self.assertTrue(form.is_valid())
        self.assertIn(
            "forms.widgets.TextInput object",
            str(form.fields.get("username").widget),
        )

    def test_newspaper_searchform_config(self):
        form = NewspaperSearchForm(data={"title": "a"})
        self.assertTrue(form.is_valid())

        self.assertIn(
            "forms.widgets.TextInput object",
            str(form.fields.get("title").widget),
        )
