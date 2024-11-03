from django import forms
from django_countries.widgets import CountrySelectWidget

from .models import Lifetime


class LifetimeForm(forms.ModelForm):
    class Meta:
        model = Lifetime
        fields = ["birth_date", "name", "country", "sex"]
        widgets = {
            "country": CountrySelectWidget(
                attrs={"class": "form-control", "id": "country"}
            )
        }
