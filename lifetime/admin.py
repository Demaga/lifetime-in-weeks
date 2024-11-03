from django.contrib import admin

from .models import Event, Lifetime

admin.site.register(Lifetime)
admin.site.register(Event)
