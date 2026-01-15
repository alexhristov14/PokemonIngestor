from common.database.elasticsearch import bulk_upsert, es

TEST_DOCUMENTS = [
    {
        "card_id": 4,
        "card_name": "Charizard",
        "last_scraped_at": "2025-01-10T14:32:00Z",
        "rarity": "Holo Rare",
        "set_name": "Base Set",
        "type": "Fire",
        "stats": {
            "grade7": {"avg": 320.5, "min": 290.0, "max": 360.0},
            "grade8": {"avg": 520.0, "min": 480.0, "max": 600.0},
            "grade9": {"avg": 2100.75, "min": 1950.0, "max": 2400.0},
            "grade9_5": {"avg": 5200.0, "min": 5000.0, "max": 5600.0},
            "grade10": {"avg": 12000.0, "min": 11000.0, "max": 14000.0},
        },
    },
    {
        "card_id": 150,
        "card_name": "Mewtwo VSTAR",
        "last_scraped_at": "2025-01-11T09:15:42Z",
        "rarity": "Ultra Rare",
        "set_name": "Crown Zenith",
        "type": "Psychic",
        "stats": {
            "grade7": {"avg": 18.5, "min": 15.0, "max": 22.0},
            "grade8": {"avg": 30.0, "min": 27.0, "max": 35.0},
            "grade9": {"avg": 55.75, "min": 50.0, "max": 65.0},
            "grade9_5": {"avg": 90.0, "min": 85.0, "max": 100.0},
            "grade10": {"avg": 150.0, "min": 140.0, "max": 175.0},
        },
    },
    {
        "card_id": 25,
        "card_name": "Pikachu",
        "last_scraped_at": "2025-01-09T18:02:11Z",
        "rarity": "Common",
        "set_name": "Jungle",
        "type": "Electric",
        "stats": {
            "grade7": {"avg": 5.25, "min": 4.0, "max": 6.5},
            "grade8": {"avg": 8.75, "min": 7.5, "max": 10.0},
            "grade9": {"avg": 14.0, "min": 12.5, "max": 17.0},
            "grade9_5": {"avg": 22.0, "min": 20.0, "max": 25.0},
            "grade10": {"avg": 40.0, "min": 38.0, "max": 45.0},
        },
    },
]

if __name__ == "__main__":
    bulk_upsert(TEST_DOCUMENTS)
