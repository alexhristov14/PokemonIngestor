import os

from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ES = Elasticsearch(ELASTICSEARCH_URL)

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
