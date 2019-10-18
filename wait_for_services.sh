#!/bin/bash
set -e

cmd="$@"

until nc -vz ${KAFKA_BOOSTRAP_SERVER_NAME} ${KAFKA_BOOSTRAP_SERVER_PORT}; do
  >&2 echo "Waiting for Kafka to be ready... - sleeping"
  sleep 2
done

>&2 echo "Kafka is up"

echo "Executing command ${cmd}"
exec $cmd