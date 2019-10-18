# FIT2107 Assignment 3

## Students

- Jonathon Vrankul
- Chee Chin Chan

# Instructions

Use `python3 WeatherForecast.py --help` to display detailed usage information.

## Example Usage

> **Note**: A valid API key must be provided for every CLI command other than `--help`.

### Commands

`python3 WeatherForecast.py --api {your_api_key} --city Melbourne --temp fahrenheit --time`

# Running tests

Use `python3 WeatherForecast.spec.py` to run the unit test suite.

# Coverage

To run and view test coverage for the program, follow these steps:

1. `pip install coverage`
1. `coverage run WeatherForecast.spec.py`
1. `coverage report`
1. Optional: `coverage html` to generate a static html report.
