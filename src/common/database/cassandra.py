import os

from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, NoHostAvailable

CASSANDRA_HOSTS = os.getenv("CASSANDRA_HOST", "cassandra").split(",")

CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))

KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "pokemon")

cluster = Cluster(CASSANDRA_HOSTS, port=CASSANDRA_PORT)
session = cluster.connect(KEYSPACE)
session.default_consistency_level = ConsistencyLevel.QUORUM


def get_cassandra_session(retries=10, delay=3):
    for i in range(retries):
        try:
            cluster = Cluster(CASSANDRA_HOSTS, port=CASSANDRA_PORT)
            session = cluster.connect(KEYSPACE)
            return session
        except NoHostAvailable:
            if i == retries - 1:
                raise
            print(f"Cassandra not available, retrying in {delay}s... ({i+1}/{retries})")
            time.sleep(delay)
