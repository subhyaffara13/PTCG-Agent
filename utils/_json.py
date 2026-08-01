
def _json(value: Any) -> str:
    """Serialize a Python value for prisma-client-py Json fields (must be a string)."""
    return json.dumps(value)

