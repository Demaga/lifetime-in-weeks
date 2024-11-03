from django.shortcuts import render

from .forms import LifetimeForm
from .models import Lifetime


def index(request):
    form = LifetimeForm()
    context = {
        "form": form,
        "lifetimes": Lifetime.objects.all().order_by("-birth_date")[:5],
    }
    return render(request, "lifetime/index.html", context)
