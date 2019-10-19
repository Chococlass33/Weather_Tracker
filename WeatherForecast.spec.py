import unittest
import mock
import json
import click
from click.testing import CliRunner
from mock import MagicMock

from WeatherForecast import *

def mock_request():
    ''' Replacement function for the request function, instead returns the stubresponse json file.'''
    with open('stubResponse.json', 'r') as f:
        return json.load(f)

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

    '''Tests for CLI commands with mocked network calls. '''

    '''The patch changes WeatherForecast.request into mock_request instead.'''

    @mock.patch('WeatherForecast.request', return_value = mock_request())
    def test_noapi(self, request):
        '''
        Test for no api given
        '''
        runner = CliRunner();
        result = runner.invoke(main, ['--city','Melbourne', '--time'])
        self.assertIsInstance(result.exception, SystemExit)
        self.assertEqual(result.output[-24:], 'Missing option "--api".\n')

    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_no_options(self, request):
        runner = CliRunner();
        result = runner.invoke(main, ['--api','3c3e7a56277f4e3239deba8785391d1a','--city', 'Melbourne'])
        self.assertEqual(result.output, "No chosen information to get\n")

    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_many_locations(self, request):
        runner = CliRunner();
        result = runner.invoke(main, ['--api','3c3e7a56277f4e3239deba8785391d1a','--city', 'Melbourne','--z','3000','--gc','90/90','--cid','1'])
        self.assertEqual(result.output, "Multiple chosen locations are specified. Please only use one of -city, -cid, -gc, -z to select a location.\n")

    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_no_locations(self, request):
        runner = CliRunner();
        result = runner.invoke(main, ['--api', '3c3e7a56277f4e3239deba8785391d1a', '--temp','celsius','--time','--pressure','--cloud','--humidity','--wind','--sunrise','--sunset'])
        self.assertEqual(result.output, "No locations are specified. Please use one of -city, -cid, -gc, -z to select a location.\n")

    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_fahrenheit(self, request):
        runner = CliRunner();
        result = runner.invoke(main, ['--api', '3c3e7a56277f4e3239deba8785391d1a','--city', 'Melbourne', '--temp','fahrenheit'])
        self.assertEqual(result.output, "The temperature is 286.65 degrees fahrenheit,  \n")

    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_gc_error_lat(self, request):
        runner = CliRunner();
        result = runner.invoke(main, ['--api', '3c3e7a56277f4e3239deba8785391d1a','--gc', '100,10'])
        self.assertIsInstance(result.exception, ValueError)


    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_gc_error_long(self, request):
        runner = CliRunner();
        result = runner.invoke(main, ['--api', '3c3e7a56277f4e3239deba8785391d1a','--gc', '10,200'])
        self.assertIsInstance(result.exception, ValueError)

    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_gc_no_error(self, request):
        runner = CliRunner();
        result = runner.invoke(main, ['--api', '3c3e7a56277f4e3239deba8785391d1a','--gc', '0,0'])
        self.assertIsNone(result.exception)

    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_extra_help(self, request):
        runner = CliRunner();
        result = runner.invoke(main, ['--api','3c3e7a56277f4e3239deba8785391d1a','--city', 'Melbourne','--help'])
        self.assertEqual(result.output[0:21], 'Usage: main [OPTIONS]')


    @mock.patch('WeatherForecast.request', return_value=mock_request())
    def test_all_options(self, request):
        runner = CliRunner();
        self.maxDiff = None
        result = runner.invoke(main, ['--api', '3c3e7a56277f4e3239deba8785391d1a', '--city', 'Melbourne', '--temp','celsius','--time','--pressure','--cloud','--humidity','--wind','--sunrise','--sunset'])
        self.assertEqual(result.output[:-2], 'On 2019-10-15 at ' + datetime.datetime.fromtimestamp(mock_request()['dt']).strftime('%H:%M:%S')+', The temperature is 286.65 degrees celsius,  Air pressure is 1014 hPa. Humidity is 82%. Cloud coverage is 75%. Sunrise time '+datetime.datetime.fromtimestamp(mock_request()['sys']['sunrise']).strftime('%H:%M:%S')+'. Sunset time '+datetime.datetime.fromtimestamp(mock_request()['sys']['sunset']).strftime('%H:%M:%S')+'. Wind speed is 3.1 from 200 degrees')
if __name__ == '__main__':
    unittest.main()
