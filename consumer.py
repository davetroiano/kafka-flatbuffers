#!/usr/bin/env python

from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer

from devx import Vehicle

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])
    consumer = Consumer(config)
    topic = "vehicle-locations"
    consumer.subscribe([topic])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                print("Waiting...")
            elif msg.error():
                print("ERROR: {error}".format(error = msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                vehicle = Vehicle.Vehicle.GetRootAs(bytearray(msg.value()), 0)
                print("Consumed event from topic {topic}: key = {key:12} vehicle ID = {vehicle_id:12} lat = {lat:12} long = {long:12}".format(
                    topic=msg.topic(),
                    key=msg.key().decode('utf-8'),
                    vehicle_id=str(vehicle.Id()),
                    lat=str(vehicle.Lat()),
                    long=str(vehicle.Long())
                ))
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
