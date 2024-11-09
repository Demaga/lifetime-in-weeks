from datetime import date

from django.shortcuts import get_object_or_404, render

from .forms import LifetimeForm
from .models import Lifetime
from .utils import weeks_between_two_dates


def index(request):
    form = LifetimeForm()
    context = {
        "form": form,
        "recent_lifetimes": Lifetime.objects.all().order_by("-created_at")[:5],
    }
    return render(request, "lifetime/index.html", context)


def celebrities(request):
    lifetimes = Lifetime.objects.filter(created_by__is_staff=True)
    context = {"lifetimes": lifetimes}
    return render(request, "lifetime/celebrities.html", context)


def detail(request, lifetime_id):
    lifetime = get_object_or_404(Lifetime, pk=lifetime_id)

    total_years = 90  # TODO: use calculated life expectancy

    # Calculate current week number if person is alive
    current_week = None
    today = date.today()
    if not lifetime.death_date:
        current_week = weeks_between_two_dates(today, lifetime.birth_date)

    # Calculate death week number if applicable
    death_week = None
    if lifetime.death_date:
        death_week = weeks_between_two_dates(
            lifetime.birth_date, lifetime.death_date
        )

    context = {
        "lifetime": lifetime,
        "years": total_years,
        "current_week": current_week,
        "death_week": death_week,
    }
    return render(request, "lifetime/lifetime.html", context)
