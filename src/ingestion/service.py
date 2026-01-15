from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import requests as r

from common.database.postgres import get_db_session
from common.models.postgres_models import CardMetadata


def fetch_card_metadata(card: dict) -> Optional[CardMetadata]:
    card_url = f"https://api.tcgdex.net/v2/en/cards/{card['id']}"

    try:
        card_details = r.get(card_url, timeout=10).json()
    except Exception:
        return None

    if not card_details:
        return None

    return CardMetadata(
        card_id=card["id"],
        card_name=card.get("name"),
        num_in_set=card_details["set"]["cardCount"].get("official"),
        evolve_from=card_details.get("evolveFrom"),
        description=card_details.get("description"),
        image=card_details.get("image"),
        set_name=card_details.get("set", {}).get("name"),
        rarity=card_details.get("rarity"),
        illustrator=card_details.get("illustrator"),
        series=card.get("set", {}).get("series"),
        reverse=card_details["variants"].get("reverse", False),
        holo=card_details["variants"].get("holo", False),
        first_edition=card_details["variants"].get("firstEdition", False),
        release_date=card.get("set", {}).get("releaseDate"),
    )


def populate_metadata_service(
    page: int = 0,
    items_per_page: int = 20,
    until_page: Optional[int] = None,
) -> None:

    with ThreadPoolExecutor(max_workers=10) as executor:
        with get_db_session() as session:
            while True:
                url = (
                    "https://api.tcgdex.net/v2/en/cards"
                    f"?pagination:page={page}&pagination:itemsPerPage={items_per_page}"
                )

                cards = r.get(url, timeout=10).json()
                if not cards:
                    break

                futures = [executor.submit(fetch_card_metadata, card) for card in cards]

                card_models = []

                for future in as_completed(futures):
                    card_meta = future.result()
                    if card_meta:
                        card_models.append(card_meta)

                session.add_all(card_models)
                session.commit()

                page += 1
                if until_page and page > until_page:
                    break
