import constants
import json
import requests

from datetime import datetime, timedelta

class TimestreamClient:
    WEATHER_DATA_URL = "http://api.openweathermap.org/data/2.5/onecall/timemachine"

    def __init__(self, client, latitude, longitude, city):
        self.client = client
        self.city = city
        self.lat = latitude
        self.lon = longitude

    def get_five_past_days(self):
        # Get the epochtimes of the last 5 days
        epochs = []
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for i in range(0, 5):
            date = current_date - timedelta(days=i)
            epochs.append(int(date.timestamp()))
        return epochs

    def prepare_record(self, timestamp, city, measure_name, measure_value):
        # Prepare record to be able to send Amazon Timestream
        return {
            'Time': str(timestamp),
            'Dimensions': [{'Name': "city", 'Value': city}],
            'MeasureName': measure_name,
            'MeasureValue': str(measure_value),
            'MeasureValueType': 'DOUBLE'
        }

    def get_weather_data(self, epoch):
        # Get sample weather data
        url = f"{self.WEATHER_DATA_URL}?lat={self.lat}&lon={self.lon}&dt={epoch}&units=metric&appid={constants.API_KEY}"
        response = requests.get(url)
        return json.loads(response.text)

    def prepare_data(self, data):
        records = []
        for hourly in data['hourly']:
            records.append(self.prepare_record(hourly['dt'] * 1000, self.city, 'temp', hourly['temp']))
            records.append(self.prepare_record(hourly['dt'] * 1000, self.city, 'feels_like', hourly['feels_like']))
            records.append(self.prepare_record(hourly['dt'] * 1000, self.city, 'humidity', hourly['humidity']))
        return records

    def write_records(self):
        for epoch in self.get_five_past_days():
            data = self.get_weather_data(epoch)
            records = self.prepare_data(data)
            try:
                # Send data to Amazon Timestream
                response = self.client.write_records(
                    DatabaseName=constants.DATABASE_NAME,
                    TableName=constants.TABLE_NAME,
                    Records=records,
                )
                print(f"WriteRecords Status: {response['ResponseMetadata']['HTTPStatusCode']}")
            except self.client.exceptions.ResourceNotFoundException:
                raise Exception("Table doesn't exists.")
            except Exception as exc:
                raise Exception(f"Unexpected error: {exc}")
