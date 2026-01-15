import logging
from typing import List

from cassandra.cluster import Cluster
from sqlalchemy import text

from common.database.elasticsearch import es
from common.database.postgres import engine

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def check_postgres() -> str:
    """Check if Postgres is reachable."""
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
    """Check if Elasticsearch is reachable."""
    try:
        return es.info()["cluster_name"]
    except Exception as e:
        return str(e)


def check_cassandra(host="cassandra", keyspace="pokemon") -> bool:
    """Check if Cassandra is reachable."""
    try:
        cluster = Cluster([host])
        session = cluster.connect(keyspace)
        session.execute("SELECT * FROM system.local")
        cluster.shutdown()
        return True
    except Exception as e:
        LOG.error(f"Cassandra health error: {e}")
        return False
