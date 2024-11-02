from django.shortcuts import render

from .models import Lifetime


def index(request):
    lifetimes = Lifetime.objects.order_by("-birth_date")[:5]
    context = {"lifetimes": lifetimes}
    return render(request, "lifetime/index.html", context)
