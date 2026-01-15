import base64
import json

from sqlalchemy.inspection import inspect


def encode_cursor(ingested_at, _id):
    payload = json.dumps(
        {
            "ingested_at": ingested_at.isoformat(),
            "id": _id,
        }
    )

    return base64.urlsafe_b64encode(payload.encode()).decode()


def decode_cursor(cursor):
    payload = json.loads(base64.urlsafe_b64decode(cursor).decode())
    return payload["ingested_at"], payload["id"]


def model_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
