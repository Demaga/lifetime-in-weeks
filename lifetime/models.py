from django.conf import settings
from django.db import models
from django_countries.fields import CountryField

from .utils import weeks_between_two_dates


class Lifetime(models.Model):
    name: models.CharField = models.CharField(
        max_length=200, null=True, blank=True
    )
    birth_date: models.DateField = models.DateField()
    death_date: models.DateField = models.DateField(null=True, blank=True)
    country = CountryField(blank=True, null=True)
    sex: models.CharField = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
        null=True,
        blank=True,
    )
    created_by: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_lifetimes",
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.name:
            return f"{self.name} - {self.birth_date}"
        else:
            return f"Lifetime starting on {self.birth_date}"

    @property
    def is_admin_created(self):
        """Check if the Lifetime was created by an admin user"""
        return self.created_by and self.created_by.is_staff


class Event(models.Model):
    title: models.CharField = models.CharField(max_length=200)
    description: models.TextField = models.TextField(blank=True)
    lifetime: models.ForeignKey = models.ForeignKey(
        Lifetime, on_delete=models.CASCADE, related_name="events"
    )
    date: models.DateField = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.date})"

    @property
    def week_number(self):
        """Calculate the week number based on event date and birth date"""
        return weeks_between_two_dates(self.date, self.lifetime.birth_date)
