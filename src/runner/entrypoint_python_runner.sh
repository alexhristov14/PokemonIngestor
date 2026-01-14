#!/bin/bash

set -e

echo "[python_runner] starting..."

if [ "${RUN_STARTUP_SCRIPTS:-true}" = "true" ]; then
	echo "[python_runner] running startup scripts"
	
	echo "[python_runner] waiting for Postgres..."
	until python3 -c "import psycopg2; psycopg2.connect('$DATABASE_URL').close()"; do
		echo "[python_runner] Postgres not ready, retrying in 5s..."
		sleep 5
	done
	
	python3 cli/init_postgres.py
	
	echo "[python_runner] waiting for Cassandra..."
	until python3 -c "from cassandra.cluster import Cluster; Cluster(['$CASSANDRA_HOST']).connect().shutdown()" 2>/dev/null; do 
		echo "[python_runner] Cassandra not ready, retrying in 5s..."
		sleep 5
	done
	
	python3 cli/init_cassandra.py

	until python3 -c "from elasticsearch import Elasticsearch; import sys; es=Elasticsearch('$ELASTICSEARCH_URL'); sys.exit(0 if es.ping() else 1)"; do
	  echo 'Waiting for Elasticsearch...'
	  sleep 2
	done

	python3 cli/init_elasticsearch.py

else
	echo "[python_runner] skipping startup scripts"
fi

echo "[python-runner] ready"

exec "$@"
