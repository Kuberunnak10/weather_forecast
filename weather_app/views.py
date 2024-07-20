from django.shortcuts import render

from weather_app.forms import WeatherForm
from weather_app.models import WeatherModel
from weather_app.utils import get_weather


def weather_view(request):
    form = WeatherForm()
    recent_cities = None

    if request.user.is_authenticated:
        recent_cities = WeatherModel.objects.filter(user=request.user).order_by('-id')[:5]

    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            if request.user.is_authenticated:
                w = WeatherModel(user=request.user, city=city)
                w.save()
            weather_data = get_weather(city)

            if isinstance(weather_data, str):
                return render(request, 'weather_app/weather.html', {
                    'form': form,
                    'error': weather_data,
                    'recent_cities': recent_cities
                })
            else:
                temp = weather_data['temperature_2m']
                wind = weather_data['wind_speed_10m']
                hum = weather_data['relative_humidity_2m']
                time = weather_data['time']

                weather_info = zip(time, temp, wind, hum)

                if request.user.is_authenticated:
                    recent_cities = WeatherModel.objects.filter(user=request.user).order_by('-id')[:5]

                return render(request, 'weather_app/weather.html', {
                    'form': form,
                    'weather_info': weather_info,
                    'recent_cities': recent_cities
                })

    return render(request, 'weather_app/weather.html', {
        'form': form,
        'recent_cities': recent_cities
    })
