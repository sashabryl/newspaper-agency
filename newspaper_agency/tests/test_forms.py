from django.contrib.auth import get_user_model
from django.forms import forms
from django.test import TestCase
from django.urls import reverse

from newspaper_agency.forms import (
    RedactorUpdateForm,
    RedactorCreateForm,
    TopicSearchForm,
    NewspaperSearchForm,
    RedactorSearchForm, NewspaperForm,
)
from newspaper_agency.models import Topic, Newspaper


class RedactorUpdateFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="freaoiewj",
            password="feoiaw408#f",
            years_of_experience=15,
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="Art")
        self.newspaper = Newspaper.objects.create(
            title="some", content="some"
        )
        self.newspaper.topics.set([self.topic])

    @staticmethod
    def get_form_data(years_of_experience: int) -> dict:
        return {
            "username": "test_2",
            "years_of_experience": years_of_experience,
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "fwa32324a@!",
            "password2": "fwa32324a@!",
            "newspapers": [1, ]
        }

    def test_form_must_work_with_correct_input(self):
        form = RedactorUpdateForm(data=self.get_form_data(15))
        self.assertTrue(form.is_valid())
        url = reverse("agency:redactor-update", args=[self.user.id])
        res = self.client.post(url, form.data)
        self.user.refresh_from_db()
        self.assertEquals(self.user.years_of_experience, 15)
        self.assertTrue(self.user.newspapers.filter(title="some").exists())

    def test_form_must_raise_validations_errors(self):
        form = RedactorUpdateForm(data=self.get_form_data(-1))
        self.assertFalse(form.is_valid())

        form = RedactorUpdateForm(data=self.get_form_data(101))
        self.assertFalse(form.is_valid())


class RedactorCreationFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="freaoiewj",
            password="feoiaw408#f",
            years_of_experience=15,
        )
        self.client.force_login(self.user)

    @staticmethod
    def get_form_data(years_of_experience: int) -> dict:
        return {
            "username": "test_2",
            "years_of_experience": years_of_experience,
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "fwa32324a@!",
            "password2": "fwa32324a@!",
        }

    def test_form_must_work_with_correct_input(self):
        form = RedactorUpdateForm(data=self.get_form_data(15))
        self.assertTrue(form.is_valid())
        url = reverse("agency:redactor-create")
        self.client.post(url, form.data)
        self.assertTrue(
            get_user_model().objects.filter(username="test_2").exists()
        )
        user = get_user_model().objects.get(username="test_2")
        self.assertEquals(user.years_of_experience, 15)
        self.assertEquals(user.first_name, "test_first")
        self.assertEquals(user.last_name, "test_last")
        self.assertTrue(user.check_password("fwa32324a@!"))

    def test_form_must_raise_validations_errors(self):
        form = RedactorUpdateForm(data=self.get_form_data(-1))
        self.assertFalse(form.is_valid())

        form = RedactorUpdateForm(data=self.get_form_data(101))
        self.assertFalse(form.is_valid())


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
                "topics": [1, ],
                "publishers": [1, ],
                "content": "some",
            }
        )
        self.assertTrue(form.is_valid())
        self.client.post(reverse("agency:newspaper-create"), form.data)
        self.assertTrue(Newspaper.objects.filter(title="test_paper").exists())

    def test_update_form_works(self):
        form = NewspaperForm(
            data={
                "title": "updated_paper",
                "topics": [1, ],
                "publishers": [2, ],
                "content": "some",
            }
        )
        self.assertTrue(form.is_valid())
        self.client.post(reverse("agency:newspaper-update", args=[1]), form.data)
        self.assertTrue(
            Newspaper.objects.filter(title="updated_paper").exists()
        )


class SearchFormsTest(TestCase):
    """Logic behind those bellow is tested in the views section"""

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
