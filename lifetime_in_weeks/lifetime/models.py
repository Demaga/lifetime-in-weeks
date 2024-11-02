from datetime import timedelta

from django.db import models


class Lifetime(models.Model):
    birth_date: models.DateField = models.DateField()

    def __str__(self):
        return f"Lifetime starting on {self.birth_date}"


class Week(models.Model):
    lifetime: models.ForeignKey = models.ForeignKey(
        Lifetime, on_delete=models.CASCADE, related_name="weeks"
    )
    week_number: models.PositiveIntegerField = models.PositiveIntegerField()

    class Meta:
        unique_together = ["lifetime", "week_number"]
        ordering = ["week_number"]

    def __str__(self):
        return (
            f"Week {self.week_number} of lifetime"
            " starting on {self.lifetime.birth_date}"
        )

    @property
    def start_date(self):
        return self.lifetime.birth_date + timedelta(
            days=7 * (self.week_number - 1)
        )


class Event(models.Model):
    title: models.CharField = models.CharField(max_length=200)
    description: models.TextField = models.TextField(blank=True)
    week: models.ForeignKey = models.ForeignKey(
        Week, on_delete=models.CASCADE, related_name="events"
    )

    def __str__(self):
        return f"{self.title} (Week {self.week.week_number})"
