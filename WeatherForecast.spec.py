import unittest
import json
from mock import MagicMock

from WeatherForecast import *

class TestWeatherForecast(unittest.TestCase):
    ''' Runs once before the test suite executes. Reads json data from store. ''' 
    @classmethod
    def setUpClass(self):
        super(TestWeatherForecast, self).setUpClass()
        self.mock = MagicMock()
        with open('stubResponse.json', 'r') as f:
            self.mock.response = json.load(f)
    
    ''' Unit tests for helper methods using static JSON data. '''
    def test_display_time(self):
        self.assertEqual(display_time(self.mock.response), "On " + datetime.datetime.fromtimestamp(
        self.mock.response['dt']
    ).strftime('%Y-%m-%d at %H:%M:%S') +", ")

    def test_display_pressure(self):
        self.assertEqual(display_pressure(self.mock.response), "Air pressure is 1014 hPa. ")

    def test_display_cloud(self):
        self.assertEqual(display_cloud(self.mock.response), "Cloud coverage is " + str(self.mock.response['clouds']['all']) + "%. ")

    def test_display_humidity(self):
        self.assertEqual(display_humidity(self.mock.response), "Humidity is " + str(self.mock.response['main']['humidity']) + "%. ")

    def test_display_wind(self):
        self.assertEqual(display_wind(self.mock.response), "Wind speed is " + str(self.mock.response['wind']['speed']) + " from " + str(self.mock.response['wind']['deg']) + " degrees.")

    def test_display_sunset(self):
        self.assertEqual(display_sunset(self.mock.response), "Sunset time " + datetime.datetime.fromtimestamp(
        self.mock.response['sys']['sunset']
    ).strftime('%H:%M:%S') +". ")

    def test_display_sunrise(self):
        self.assertEqual(display_sunrise(self.mock.response), "Sunrise time " + datetime.datetime.fromtimestamp(
        self.mock.response['sys']['sunrise']
    ).strftime('%H:%M:%S') +". ")

    ''' TODO: Tests for CLI commands with mocked network calls. '''
    
if __name__ == '__main__':
    unittest.main()
