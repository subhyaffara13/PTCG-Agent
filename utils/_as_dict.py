
def _as_dict(response: bytes | dict) -> dict:
    return json.loads(response) if isinstance(response, bytes) else response

