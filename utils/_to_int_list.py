import json

def _to_int_list(v: str) -> list[int]:
    return json.loads(v)

