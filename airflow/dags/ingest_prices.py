import os
from datetime import datetime

from airflow.providers.docker.operators.docker import DockerOperator

from airflow import DAG

DATABASE_URL = os.getenv("DATABASE_URL")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")

with DAG(
    "ingest_pokemon_prices",
    start_date=datetime(2025, 1, 7),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    run_spider = DockerOperator(
        task_id="run_scrapy_spider",
        image="pokemondataingestor-crawler:latest",
        command="scrapy crawl pokechartspider",
        network_mode="pokemondataingestor_default",
        auto_remove=True,
        environment={
            "DATABASE_URL": DATABASE_URL,
            "ELASTICSEARCH_URL": ELASTICSEARCH_URL,
        },
    )


#   ingest = BashOperator(
#       task_id="run_ingestion",
#       bash_command="python3 /opt/airflow/ingestion/main.py",
#   )
