import json

def serialize_messages(messages: Sequence[object]) -> str | None:
    """Round-trip a sequence of message dicts through ``stringify_message``."""
    serialized = [
        json.loads(s) for s in (stringify_message(m) for m in messages) if s is not None
    ]
    return json.dumps(serialized) if serialized else None

