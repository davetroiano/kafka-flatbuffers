#!/usr/bin/env python

from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer
import flatbuffers

from devx import Vehicle

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    producer = Producer(config)

    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value()))

    topic = "vehicle-locations"
    count = 0

    # TODO: add event variation, instantiate per record
    builder = flatbuffers.Builder(1024)
    id = builder.CreateString("997ce366-7452-4bea-ad43-b35561335074")
    Vehicle.Start(builder)
    Vehicle.AddId(builder, id)
    Vehicle.AddLat(builder, 42.3601)
    Vehicle.AddLong(builder, 71.0589)
    vehicle = Vehicle.End(builder)
    builder.Finish(vehicle)
    buf = builder.Output()

    for _ in range(10):
        producer.produce(topic, key='997ce366-7452-4bea-ad43-b35561335074', value=bytes(buf), callback=delivery_callback)
        count += 1

    producer.poll(10000)
    producer.flush()
