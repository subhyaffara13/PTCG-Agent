import json
from typing import Any

def _serialize_metadata_for_prisma(metadata: Any) -> str:
    """
    Encode a `metadata` payload for the `Json?` column.

    `metadata` is typed `Optional[Any]`, so callers may send dicts, lists,
    or JSON scalars (including plain Python strings like `"hello"`).
    prisma-client-python rejects raw Python values on `Json?` columns
    (`MissingRequiredValueError` / `DataError`), and Postgres `jsonb`
    rejects bare-word strings as invalid JSON — so always `json.dumps`,
    regardless of input type. Roundtrip on read deserializes back to the
    original Python value.
    """
    return json.dumps(metadata)

