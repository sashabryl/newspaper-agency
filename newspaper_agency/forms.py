from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from newspaper_agency.models import Topic, Newspaper


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "by title"}),
        label="",
    )


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "by username"}),
        label="",
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "by name"}),
        label="",
    )


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class RedactorCreateForm(UserCreationForm):
    newspapers = forms.ModelMultipleChoiceField(
        queryset=Newspaper.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    years_of_experience = forms.IntegerField(max_value=100, initial=0)

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "years_of_experience",
            "email",
            "newspapers",
        )


class RedactorUpdateForm(forms.ModelForm):
    newspapers = forms.ModelMultipleChoiceField(
        queryset=Newspaper.objects.prefetch_related("publishers").all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    years_of_experience = forms.IntegerField(max_value=100, initial=0)

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "years_of_experience",
            "email",
            "newspapers",
        )
