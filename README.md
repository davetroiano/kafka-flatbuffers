# Produce and Consume FlatBuffers-formatted data to Kafka

This is a simple example showing how to produce and consume [FlatBuffers](https://flatbuffers.dev/)-formatted data in Kafka using Python.

## Running the example

1. Docker should be installed and running
2. Install the [Confluent CLI](https://docs.confluent.io/confluent-cli/current/install.html)
3. Start Kafka in Docker and note the `Plaintext Ports` output: `confluent local kafka start`
4. Add the port from the previous step to `properties.ini` file
5. Produce: `./producer.py properties.ini`
6. Consume: `./consumer.py properties.ini`

## Regenerating FlatBuffers client code

If you change the schema in `vehicle.fbs`, you'll first need the `flatc` compiler. On Mac:

1. `brew install cmake`
2. `git clone https://github.com/google/flatbuffers.git`
3. `cd flatbuffers`
4. `cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release`
5. `make`
6. The `./flatc` binary can be used to compile

To compile the sample schema in this repo for Python:

```commandline
rm -rf devx
/path/to/flatc --python vehicle.fbs
```