from django.contrib import admin

from .models import Event, Lifetime, Week

admin.site.register(Lifetime)
admin.site.register(Week)
admin.site.register(Event)
