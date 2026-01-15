from common.database.postgres import get_db_session
from common.models.postgres_models import CardMetadata, RawCardPrice
from common.utils.converter import model_to_dict
from sqlalchemy import select

def link_raw_and_metadata(db, limit = 20, cursor = None):
    query = (
        db.query(RawCardPrice)
        .order_by(RawCardPrice.ingested_at.desc(), RawCardPrice.id.desc())
        .limit(limit)
    )

    if cursor:
        ingested_at, card_id = cursor

        query = query.filter()

if __name__ == '__main__':
    with get_db_session() as session:
        card_name_raw = session.execute(select(RawCardPrice.card_name)).scalars().all()[100]
        card_name_raw = card_name_raw.lower().split("-")[0]
        print(len(session.execute(select(CardMetadata).where(CardMetadata.card_name.ilike(card_name_raw))).scalars().all()))
