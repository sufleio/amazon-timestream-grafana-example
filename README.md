This example demonstrates how to load sample data to Amazon Timestream with using Python and boto3. We used [One Call API](https://openweathermap.org/api/one-call-api) of OpenWeatherMap to fetch temperature, feels-like temperature and humidity data for last five days.

## Requirements
- python +3.7
- pip

## Installation
After cloning the project, in the main directory:
- `virtualenv -p python3 venv`
- `source venv/bin/activate`
- `pip install -r requirements`

## Example Usage
In the constants.py file, you should define your AWS credentials, OpenWeatherMap access token and the latitude and longitude informations of the desired city. You can find a couple of cities defined in the file, e.g. for Istanbul, you should run;

`python3 main.py --city Istanbul`

## Grafana Sample Queries

### macros:
- $__database = weatherDB
- $__table = weathertable
- $__measure = feels_like or temp

### For multiline graph:
- Query1: SELECT time, measure_value::double as temperature FROM $__database.$__table WHERE city='Istanbul' AND measure_name='$__measure'
- Query2: SELECT time, measure_value::double as feels_like_temperature FROM $__database.$__table  WHERE city='Istanbul' AND measure_name='$__measure'
### For temperature average stat:
- SELECT AVG(measure_value::double)
FROM $__database.$__table
WHERE city='Istanbul' AND measure_name='$__measure'