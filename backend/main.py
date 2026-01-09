import logging
import os
from typing import List

from elasticsearch import Elasticsearch
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")

engine = create_engine(DATABASE_URL)
es = Elasticsearch(ELASTICSEARCH_URL)

TABLES = {
    "raw_card_prices": """
        CREATE TABLE IF NOT EXISTS raw_card_prices (
            card_id SERIAL PRIMARY KEY,
            card_name TEXT,
            set_name TEXT,
            raw_price REAL,
            grade7_price REAL,
            grade8_price REAL,
            grade9_price REAL,
            grade9_5_price REAL,
            grade10_price REAL,
            scraped_at TIMESTAMP,
            ingested_at TIMESTAMP DEFAULT NOW()
        );
    """,
    "card_metadata": """
        CREATE TABLE IF NOT EXISTS card_metadata (
            card_id SERIAL PRIMARY KEY,
            set_name TEXT,
            pokemon_type TEXT,
            rarity TEXT,
            illustrator TEXT,
            series TEXT,
            numbers_in_set SMALLINT,
            release_date TEXT
        );
    """,
    "processed_card_price_stats": """
        CREATE TABLE IF NOT EXISTS processed_card_price_stats (
            id SERIAL PRIMARY KEY,
            card_id INT REFERENCES card_metadata(card_id),
            avg_price REAL,
            min_price REAL,
            max_price REAL,
            price_grade_distribution JSONB,
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """,
    "card_price_history": """
        CREATE TABLE IF NOT EXISTS card_price_history (
            id SERIAL PRIMARY KEY,
            card_id INT REFERENCES processed_card_price_stats(id),
            grade SMALLINT,
            price REAL,
            recorded_at TIMESTAMP DEFAULT NOW()
        );
    """,
}


# -----------------------------
# Functions
# -----------------------------
def create_all_tables() -> None:
    """Create all tables in the database."""
    try:
        with engine.begin() as conn:
            for table_name, ddl in TABLES.items():
                conn.execute(text(ddl))
                LOG.info(f"Created table {table_name}")
    except Exception as e:
        LOG.error(f"Error creating tables: {e}")
        raise


def check_postgres() -> str:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "ok"
    except Exception as e:
        return str(e)


def check_postgres_table(table_names: List[str]) -> dict:
    """Check if specific tables exist in Postgres."""
    results = {}
    try:
        with engine.connect() as conn:
            for table in table_names:
                query = text(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.tables
                        WHERE table_name = :table
                    )
                    """
                )
                result = conn.execute(query, {"table": table}).scalar()
                results[table] = result
    except Exception as e:
        LOG.error(f"Error checking tables: {e}")
        return {"error": str(e)}
    return results


def check_elasticsearch() -> str:
    try:
        return es.info()["cluster_name"]
    except Exception as e:
        return str(e)


@app.get("/")
def health_check():
    return {
        "postgres": check_postgres(),
        "elasticsearch": check_elasticsearch(),
    }


@app.get("/create_tables")
def create_tables():
    create_all_tables()
    return {"status": "tables created"}
