from django import forms

from weather_app.models import WeatherModel


class WeatherForm(forms.ModelForm):
    class Meta:
        model = WeatherModel
        fields = ['city']
