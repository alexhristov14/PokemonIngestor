import os

from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
es = Elasticsearch(ELASTICSEARCH_URL)

INDEX_NAME = "pokemon-index"
MAX_RETRIES = 10

INDEX_BODY = {
    "settings": {"number_of_shards": 3, "number_of_replicas": 2},
    "mappings": {
        "properties": {
            "card_id": {"type": "integer"},
            "card_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "set_name": {"type": "keyword"},
            "type": {"type": "keyword"},
            "rarity": {"type": "keyword"},
            "stats": {
                "properties": {
                    "grade7": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                    "grade8": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                    "grade9": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                    "grade9_5": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                    "grade10": {
                        "properties": {
                            "avg": {"type": "float"},
                            "min": {"type": "float"},
                            "max": {"type": "float"},
                        }
                    },
                }
            },
            "last_scraped_at": {"type": "date"},
        }
    },
}

# Example document

# {
# "card_id": 123,
# "card_name": "Pikachu",
# "set_name": "Base Set",
# "type": "Electric",
# "rarity": "Rare",
# "stats": {
#   "grade7": {"avg": 10.5, "min": 8.0, "max": 12.0},
#   "grade8": {"avg": 12.0, "min": 10.0, "max": 14.5},
#   "grade9": {"avg": 20.0, "min": 18.0, "max": 22.0},
#   "grade9_5": {"avg": 50.0, "min": 45.0, "max": 55.0},
#   "grade10": {"avg": 120.0, "min": 110.0, "max": 130.0}
# },
# "last_scraped_at": "2026-01-09T11:00:00Z"
# }

if __name__ == "__main__":
    for attempt in range(MAX_RETRIES):
        try:
            if es.ping():
                print("Connected to Elasticsearch!")
                break
        except ConnectionError:
            pass
        print(f"Waiting for Elasticsearch ({attempt + 1}/{MAX_RETRIES})...")
        time.sleep(3)
    else:
        raise RuntimeError("Elasticsearch not reachable after several retries")

    if es.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' exists. Deleting...")
        es.indices.delete(index=INDEX_NAME)

    # Create index with mapping
    es.indices.create(index=INDEX_NAME, body=INDEX_BODY)
    print(f"Index '{INDEX_NAME}' created successfully!")

    # Verify mapping
    mapping = es.indices.get_mapping(index=INDEX_NAME)
    print("Current mapping for index:")
    print(mapping)
