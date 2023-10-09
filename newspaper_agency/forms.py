from django import forms
from django.contrib.auth import get_user_model

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
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"
