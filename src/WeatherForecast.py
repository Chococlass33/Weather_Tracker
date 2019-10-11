import argparse
import sys


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='A simple weather forecasting program.')

    parser.add_argument('-api', required=True,
                        help='openweather api key')

    parser.add_argument('-city',
                        help='city name')

    parser.add_argument('-gc',
                        help='geographic coordinates')

    parser.add_argument('-z',
                        help='zip code')

    parser.add_argument('-time',
                        help='time')

    parser.add_argument('-temp',
                        help='temperature (celsius, fahrenheit) default is celsius')

    parser.add_argument('-pressure',
                        help='includes pressure information')

    parser.add_argument('-cloud',
                        help='includes cloud information')

    parser.add_argument('-humidity',
                        help='includes humidity information')

    parser.add_argument('-wind',
                        help='includes wind information')

    parser.add_argument('-sunset',
                        help='includes sunset time')

    parser.add_argument('-sunrise',
                        help='includes sunrise time')
    # ...Create your parser as you like...
    return parser.parse_args(args)


if __name__ == "__main__":
    print('WeatherForecast ran with ' + str(len(sys.argv) - 1) + ' args.')
    parser = parse_args(sys.argv[1:])
