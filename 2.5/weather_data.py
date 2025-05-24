import json, requests

def get_weather_data(city_name):
    API_KEY = 'aef454789ee3d0bad82fee47b0613904'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(url).text
    data = json.loads(response)

    if len(data) == 2 and data['cod'] == '404':
        return "Неправильное название города"
    else:
        return f'Город: {data["name"]}\nТемпература: {data["main"]["temp"]} °C\nОписание: {data["weather"][0]["description"]}'