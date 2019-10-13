import click
import requests

'''Use a valid API key here. The default value is only a sample.'''
API_KEY = ''


def dispatch_weather_request(location, location_type, time, temp, pressure, cloud, humidity, wind, sunset, sunrise, api=API_KEY):
    url = 'http://api.openweathermap.org/data/2.5/weather'

    location_query = ''

    def location_switch(argument):
        switch = {
            'city': "q",
            'cid': "id",
            'gc': "lat",
            'z': "zip",
        }
        return switch.get(argument, "Invalid location type argument, must be one of city, cid, gc, z.")

    try:
        location_query = location_switch(location_type)
    except:
        print("Invalid location argument exception: please use one of city, cid, gc, z.")

    temperature_type = 'metric'
    if (temp == 'fahrenheit'):
        temperature_type = 'imperial'

    query_params = {
        location_query: location,
        'units': temperature_type,
        'APPID': api,
    }

    response = requests.get(url, params=query_params)

    '''Prints the response for debugging purposes'''
    print(response)

    return response.json()['main']['temp']


@click.command()
@click.option(
    '--city', '-city',
    help='city name to retrieve weather data for, e.g. Melbourne',
)
@click.option(
    '--cid', '-cid',
    help='unique city identifier',
)
@click.option(
    '--gc', '-gc',
    help='geographical coordinates for a city',
)
@click.option(
    '--z', '-z',
    help='city zipcode with optional 2 character location code, e.g. 3000,au for Melbourne, Australia',
)
@click.option(
    '--time', '-time',
    help='time of day, must be in the past (defaults to present time)',
)
@click.option(
    '--temp', '-temp',
    help='celsius or fahrenheit (default celsius)',
)
@click.option(
    '--pressure', '-pressure',
    help='displays air pressure information',
)
@click.option(
    '--cloud', '-cloud',
    help='displays cloud information',
)
@click.option(
    '--humidity', '-humidity',
    help='displays humidity information',
)
@click.option(
    '--wind', '-wind',
    help='displays wind speed',
)
@click.option(
    '--sunset', '-sunset',
    help='displays sunset time',
)
@click.option(
    '--sunrise', '-sunrise',
    help='displays sunrise time',
)
@click.option(
    '--api',
    help='your API key for the OpenWeatherMap API',
)
def main(city, cid, gc, z, time, temp, pressure, cloud, humidity, wind, sunset, sunrise, api):
    ''' Checking if too many location arguments were provided. '''
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
        location, location_type, time, temp, pressure, cloud, humidity, wind, sunset, sunrise, API_KEY)

    print(
        f"The temperature is {weather} degrees {'fahrenheit' if (temp == 'fahrenheit') else 'celsius'}.")


if __name__ == "__main__":
    main()
