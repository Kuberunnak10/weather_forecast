import pytest
from django.urls import reverse

from weather_app.utils import get_weather


@pytest.mark.django_db
def test_get_weather_valid_city(mocker):
    city = 'Москва'
    mock_response_geo = {
        'results': [{
            'latitude': 55.7558,
            'longitude': 37.6176,
            'timezone': 'Europe/Moscow'
        }]
    }
    mock_response_weather = {
        'hourly': {
            'time': [
                '2024-07-20 12:00:00',
                '2024-07-20 13:00:00',
                '2024-07-20 14:00:00',
                '2024-07-20 15:00:00',
                '2024-07-20 16:00:00'
            ],
            'temperature_2m': [20, 21, 22, 23, 24],
            'wind_speed_10m': [5, 6, 7, 8, 9],
            'relative_humidity_2m': [55, 60, 65, 70, 75]
        }
    }

    mocker.patch('requests.get', side_effect=[
        mocker.Mock(json=lambda: mock_response_geo),
        mocker.Mock(json=lambda: mock_response_weather)
    ])

    weather_data = get_weather(city)
    assert 'temperature_2m' in weather_data
    assert 'wind_speed_10m' in weather_data
    assert 'relative_humidity_2m' in weather_data
    assert len(weather_data['temperature_2m']) == 4


@pytest.mark.django_db
def test_get_weather_invalid_city(mocker):
    city = 'НекорректныйГород'
    mock_response_geo = {'results': []}

    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: mock_response_geo))

    weather_data = get_weather(city)
    assert weather_data == "Город 'НекорректныйГород' не найден."


@pytest.mark.django_db
def test_weather_view_authenticated_user(client, django_user_model):
    username = 'testuser'
    password = 'password'
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    response = client.post(reverse('weather'), {'city': 'Москва'})

    assert response.status_code == 200
    assert 'weather_info' in response.context
    assert 'recent_cities' in response.context

    recent_cities = response.context['recent_cities']
    assert len(recent_cities) == 1
    assert recent_cities[0].city == 'Москва'


@pytest.mark.django_db
def test_weather_view_unauthenticated_user(client):
    response = client.post(reverse('weather'), {'city': 'Москва'})

    assert response.status_code == 200
    assert 'weather_info' in response.context
    assert 'recent_cities' in response.context
