from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ["-years_of_experience"]

    def __str__(self) -> str:
        return f"{self.username} ({self.years_of_experience} years of experience)"


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topics = models.ManyToManyField("Topic", related_name="newspapers")
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="newspapers"
    )

    class Meta:
        ordering = ["-published_date"]

    def __str__(self) -> str:
        return self.title