import argparse
import boto3

import constants
from clients import TimestreamClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", help="City")
    args = parser.parse_args()

    city = args.city
    if not city:
        raise ValueError("Invalid argument.")

    try:
        coordinates = constants.CITIES_MAPPING[city]
    except KeyError:
        raise ValueError("Invalid selection.")

    client = boto3.client(
        'timestream-write',
        aws_access_key_id=constants.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=constants.AWS_SECRET_ACCESS_KEY,
        region_name=constants.AWS_DEFAULT_REGION
    )

    timestream_client = TimestreamClient(client, coordinates['lat'], coordinates['lon'], args.city)
    # Write sample data to Amazon Timestream
    timestream_client.write_records()


if __name__ == '__main__':
    main()
