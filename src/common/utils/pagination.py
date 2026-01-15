import base64
import json
from datetime import datetime
from typing import Any, List, Optional, Tuple, TypeVar

from sqlalchemy.orm import Query
from sqlalchemy.sql import ColumnElement

T = TypeVar("T")


class CursorPagination:
    def __init__(
        self,
        base_query: Query,
        order_by: List[ColumnElement],
        cursor_columns: List[ColumnElement],
        limit: int = 20,
    ) -> None:
        if len(order_by) != len(cursor_columns):
            raise ValueError("order_by and cursor_columns must have the same length")

        self.base_query = base_query
        self.order_by = order_by
        self.cursor_columns = cursor_columns
        self.limit = limit

    def encode_cursor(self, row: Any) -> str:
        values = []

        for col in self.cursor_columns:
            value = getattr(row, col.key)

            if isinstance(value, datetime):
                value = value.isoformat()

            values.append(value)

        payload = json.dumps(values)
        return base64.urlsafe_b64encode(payload.encode()).decode()

    def decode_cursor(self, cursor: str) -> Tuple:
        raw_values = json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())

        decoded = []
        for value in raw_values:
            if isinstance(value, str) and "T" in value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass
            decoded.append(value)

        return tuple(decoded)

    def page(self, cursor: Optional[str] = None) -> Tuple[List[T], Optional[str]]:
        query = self.base_query

        if cursor:
            decoded_cursor = self.decode_cursor(cursor)
            query = query.filter(tuple(self.cursor_columns) < decoded_cursor)

        query = query.order_by(*self.order_by).limit(self.limit)

        items = query.all()
        next_cursor = None

        if items:
            next_cursor = self.encode_cursor(items[-1])

        return items, next_cursor
