#!/bin/bash

set -e

echo "[python_runner] starting..."

until cqlsh "$CASSANDRA_HOST" -e "describe keyspaces" >/dev/null 2>&1; do 
	echo "[python-runner] Cassandra not ready, retrying in 5s..."
  	sleep 5
done

if [ "${RUN_STARTUP_SCRIPTS:-true}" = "true" ]; then
	echo "[python_runner] running startup scripts"
	# python3 cli/init_postgres.py
	python3 cli/init_cassandra.py
	# python3 cli/init_elasticsearch.py

else
	echo "[python_runner] skipping startup scripts"
fi

echo "[python-runner] ready"

exec "$@"
