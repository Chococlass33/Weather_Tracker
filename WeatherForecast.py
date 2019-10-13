import click
import requests
import datetime


def dispatch_weather_request(location, location_type, time, temp, pressure, cloud, humidity, wind, sunset, sunrise, api):
    url = 'http://api.openweathermap.org/data/2.5/weather'

    location_query = ''

    def location_switch(argument):
        switch = {
            'city': "q",
            'cid': "id",
            'gc': "gc",
            'z': "zip",
        }
        return switch.get(argument, "Invalid location type argument, must be one of city, cid, gc, z.")

    try:
        location_query = location_switch(location_type)
    except:
        print("Invalid location argument exception: please use one of city, cid, gc, z.")

    temperature_type = 'metric'
    if temp == 'fahrenheit':
        temperature_type = 'imperial'

    query_params = {
        location_query: location,
        'units': temperature_type,
        'APPID': api,
    }

    if location_type == 'gc':
        coordinates = [location.strip() for location in location.split(',')]
        query_params.pop('gc', None)
        if -90 <= int(coordinates[0]) <= 90:
          query_params['lat'] = int(coordinates[0])
        else:
          raise ValueError('Latitude out of range. Must be between -90 and 90.')

        if -180 <= int(coordinates[1]) <= 180:
          query_params['lon'] = int(coordinates[1])
        else:
          raise ValueError('Longitude out of range. Must be between -180 and 180.')


    response = requests.get(url, params=query_params)

    return response.json()


@click.command()
@click.option(
    '--api', required=True,
    help='your API key for the OpenWeatherMap API',
)
@click.option(
    '--city', '-city',
    help='city name to retrieve weather data for, e.g. Melbourne',
)
@click.option(
    '--cid', '-cid', type=int,
    help='unique city identifier',
)
@click.option(
    '--gc', '-gc',
    help='geographical coordinates for a city, comma-separated, no spaces, e.g. 100.37,-37.54',
)
@click.option(
    '--z', '-z',
    help='city zipcode with optional 2 character location code, e.g. 3000,au for Melbourne, Australia',
)
@click.option(
    '--temp', '-temp',
    help='celsius or fahrenheit (default celsius)',
)
@click.option('--time', '-time', is_flag=True, help='displays the current time')
@click.option('--pressure', '-pressure', is_flag=True, help='displays air pressure information')
@click.option('--cloud', '-cloud', is_flag=True, help='displays cloud information')
@click.option('--humidity', '-humidity', is_flag=True, help='displays humidity information',)
@click.option('--wind', '-wind', is_flag=True, help='displays wind speed',)
@click.option('--sunset', '-sunset', is_flag=True, help='displays sunset time',)
@click.option('--sunrise', '-sunrise', is_flag=True, help='displays sunrise time',)
def main(city, cid, gc, z, time, temp, pressure, cloud, humidity, wind, sunset, sunrise, api):
    ''' This program displays weather information retrieved from the OpenWeatherMap API. See below for a list of options. '''
    num_location_args = 0
    location_type = ''
    if (city):
        num_location_args += num_location_args + 1
        location_type = 'city'
        location = city
    if (cid):
        num_location_args += num_location_args + 1
        location_type = 'cid'
        location = cid
    if (gc):
        num_location_args += num_location_args + 1
        location_type = 'gc'
        location = gc
    if (z):
        num_location_args += num_location_args + 1
        location_type = 'z'
        location = z

    if (num_location_args > 1):
        print('Multiple chosen locations are specified. Please only use one of -city, -cid, -gc, -z to select a location.')
        return 0

    weather = dispatch_weather_request(
        location, location_type, time, temp, pressure, cloud, humidity, wind, sunset, sunrise, api)

    print(f"The temperature is {weather['main']['temp']} degrees {'fahrenheit' if (temp == 'fahrenheit') else 'celsius'}, {weather['weather'][0]['description']}. {display_pressure(weather) if (pressure) else ''}{display_humidity(weather) if (humidity) else ''}{display_cloud(weather) if (cloud) else ''}{display_sunrise(weather) if (sunrise) else ''}{display_sunset(weather) if (sunset) else ''}{display_wind(weather) if (wind) else ''}")


''' Helper functions for displaying flag-based conditional data .'''


def display_time(data):
    return "On " + datetime.datetime.fromtimestamp(
        data['dt']
    ).strftime('%Y-%m-%d at %H:%M:%S') + ', '


def display_pressure(data):
    return "Air pressure is " + str(data['main']['pressure']) + ' hPa. '


def display_cloud(data):
    return "Cloud coverage is " + str(data['clouds']['all']) + '%. '


def display_humidity(data):
    return "Humidity is " + str(data['main']['humidity']) + '%. '


def display_wind(data):
    return "Wind speed is " + str(data['wind']['speed']) + ' from ' + str(data['wind']['deg']) + ' degrees.'


def display_sunset(data):
    return "Sunset time " + datetime.datetime.fromtimestamp(
        data['sys']['sunset']
    ).strftime('%H:%M:%S') + '. '

def display_sunrise(data):
    return "Sunrise time " + datetime.datetime.fromtimestamp(
        data['sys']['sunrise']
    ).strftime('%H:%M:%S') + '. '


if __name__ == "__main__":
    main()
