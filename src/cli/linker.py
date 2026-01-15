import re

from sqlalchemy import func, select

from common.database.postgres import get_db_session
from common.models.postgres_models import CardMetadata, RawCardPrice
from common.utils.converter import decode_cursor, encode_cursor
from common.utils.pagination import CursorPagination


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


if __name__ == "__main__":
    with get_db_session() as session:
        paginator = CursorPagination(
            base_query=session.query(RawCardPrice),
            order_by=[
                RawCardPrice.ingested_at.desc(),
                RawCardPrice.id.desc(),
            ],
            cursor_columns=[
                RawCardPrice.ingested_at,
                RawCardPrice.id,
            ],
        )

        cursor = None

        while True:
            rows, cursor = paginator.page(cursor)

            for row in rows:
                pokemon_name = normalize(row.card_name.split("-")[0])
                set_name = normalize(row.set_name)

                print(f"pokemon: {pokemon_name}")
                print(f"set: {set_name}")

                results = (
                    session.query(CardMetadata)
                    .filter(
                        func.lower(CardMetadata.card_name).ilike(f"%{pokemon_name}%"),
                        func.lower(CardMetadata.set_name).ilike(f"%{set_name}%"),
                    )
                    .limit(5)
                    .all()
                )

                if results:
                    print(results)
                    break

            if not rows:
                break
