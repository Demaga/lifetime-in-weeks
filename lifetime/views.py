from datetime import date

from django.shortcuts import get_object_or_404, render

from .forms import LifetimeForm
from .models import Lifetime


def index(request):
    form = LifetimeForm()
    context = {
        "form": form,
        "lifetimes": Lifetime.objects.all().order_by("-birth_date")[:5],
    }
    return render(request, "lifetime/index.html", context)


def detail(request, lifetime_id):
    lifetime = get_object_or_404(Lifetime, pk=lifetime_id)

    total_years = 90  # TODO: use calculated life expectancy

    # Calculate current week number if person is alive
    today = date.today()
    current_week = (
        ((today - lifetime.birth_date).days // 7) + 1
        if not lifetime.death_date
        else None
    )

    # Calculate death week number if applicable
    death_week = None
    if lifetime.death_date:
        death_week = (
            (lifetime.death_date - lifetime.birth_date).days // 7
        ) + 1

    context = {
        "lifetime": lifetime,
        "years": range(total_years),
        "current_week": current_week,
        "death_week": death_week,
    }
    return render(request, "lifetime/lifetime.html", context)
