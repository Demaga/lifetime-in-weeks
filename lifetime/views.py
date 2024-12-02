from datetime import date, timedelta

from django.shortcuts import get_object_or_404, redirect, render

from .forms import LifetimeForm
from .models import Lifetime, LifetimeExpectancy
from .utils import weeks_between_two_dates


def index(request):
    if request.method == "POST":
        form = LifetimeForm(request.POST)
        if form.is_valid():
            birth_year = form.cleaned_data["birth_date"]
            if birth_year:
                birth_year = birth_year.year
                if birth_year > 2024:
                    birth_year = 2024
                elif birth_year < 1960:
                    birth_year = 1960
            else:
                birth_year = 2023

            country = form.cleaned_data["country"]
            present_countries = (
                LifetimeExpectancy.objects.order_by()
                .values_list("country")
                .distinct()
            )
            if country not in present_countries:
                country = None

            sex = form.cleaned_data["sex"] or "O"
            life_expectancy = LifetimeExpectancy.objects.filter(
                birth_year=birth_year, sex=sex, country=country
            ).first()

            lifetime_data = form.cleaned_data
            lifetime_data["life_expectancy"] = life_expectancy.life_expectancy

            lifetime = Lifetime(**lifetime_data)
            lifetime.save()

            return redirect("lifetime:detail", lifetime_id=lifetime.id)

    else:
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


def detail(request, lifetime_id: int | None = None, slug: str | None = None):
    if lifetime_id:
        lifetime = get_object_or_404(Lifetime, pk=lifetime_id)
    elif slug:
        lifetime = Lifetime.get_by_slug(slug)

    total_years = 90  # TODO: use calculated life expectancy

    # Calculate current week number if person is alive
    current_week = None
    today = date.today()
    if not lifetime.death_date:
        current_week = weeks_between_two_dates(today, lifetime.birth_date)

    # Calculate death week number if applicable
    death_week = None
    death_event = None
    if lifetime.death_date:
        death_week = weeks_between_two_dates(
            lifetime.birth_date, lifetime.death_date
        )
        death_age = lifetime.death_date.year - lifetime.birth_date.year
        death_event = f"{lifetime.name} died on \
            {lifetime.death_date.strftime('%b %d, %Y')} aged {death_age}"

    # Calculate expected death week number
    expected_death_days = int(lifetime.life_expectancy * 365.25)
    expected_death_date = lifetime.birth_date + timedelta(
        days=expected_death_days
    )
    expected_death_week = weeks_between_two_dates(
        lifetime.birth_date, expected_death_date
    )

    context = {
        "lifetime": lifetime,
        "years": total_years,
        "current_week": current_week,
        "death_week": death_week,
        "death_event": death_event,
        "expected_death_week": expected_death_week,
    }
    return render(request, "lifetime/lifetime.html", context)
