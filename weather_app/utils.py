import datetime

import requests


def get_weather(city):
    # Получение широты и долготы по названию города
    resp = requests.get(
        f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru&format=json').json()
    if not resp.get('results'):
        return f"Город '{city}' не найден."

    latitude = resp['results'][0]['latitude']
    longitude = resp['results'][0]['longitude']
    timezone = resp['results'][0]['timezone']

    # Получение прогноза погоды по широте и долготе
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m,wind_speed_10m,relative_humidity_2m',
        'timezone': timezone
    }

    response = requests.get(url, params=params).json()

    if 'hourly' not in response:
        return "Данные о погоде недоступны."

    # Установка часового пояса UTC+3
    tz = datetime.timezone(datetime.timedelta(hours=3))

    # Текущие дата и время в UTC+3
    now = datetime.datetime.now(tz)

    # Фильтрация данных на следующие 5 часов
    forecast = {
        'temperature_2m': [],
        'wind_speed_10m': [],
        'relative_humidity_2m': [],
        'time': []
    }

    for i, forecast_time in enumerate(response['hourly']['time']):
        forecast_datetime = datetime.datetime.fromisoformat(forecast_time).replace(
            tzinfo=datetime.timezone.utc).astimezone(tz)
        if now <= forecast_datetime < now + datetime.timedelta(hours=5):
            forecast['time'].append(
                forecast_datetime.strftime('%Y-%m-%d %H:%M'))  # Форматируем время в удобочитаемый формат
            forecast['temperature_2m'].append(response['hourly']['temperature_2m'][i])
            forecast['wind_speed_10m'].append(response['hourly']['wind_speed_10m'][i])
            forecast['relative_humidity_2m'].append(response['hourly']['relative_humidity_2m'][i])

    return forecast
