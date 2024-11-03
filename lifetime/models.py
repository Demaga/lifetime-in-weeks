from django.db import models
from django_countries.fields import CountryField


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

    def __str__(self):
        if self.name:
            return f"{self.name} - {self.birth_date}"
        else:
            return f"Lifetime starting on {self.birth_date}"


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
        delta = self.date - self.lifetime.birth_date
        return (delta.days // 7) + 1
