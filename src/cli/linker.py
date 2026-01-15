from sqlalchemy import select

from common.database.postgres import get_db_session
from common.models.postgres_models import CardMetadata, RawCardPrice
from common.utils.converter import decode_cursor, encode_cursor
from common.utils.pagination import CursorPagination

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
        total = 0

        while True:
            rows, cursor = paginator.page(cursor)
            total += len(rows)
            print(f"current total: {total}")

            if len(rows) == 0:
                break


#       card_name_raw = session.execute(select(RawCardPrice.card_name)).scalars().all()[100]
#       card_name_raw = card_name_raw.lower().split("-")[0]
#       print(len(session.execute(select(CardMetadata).where(CardMetadata.card_name.ilike(card_name_raw))).scalars().all()))
