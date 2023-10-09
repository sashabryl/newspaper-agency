from django import forms


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

