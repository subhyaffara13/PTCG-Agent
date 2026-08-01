
def _deserialize_json_list(data: Any) -> Optional[List[Dict[str, Any]]]:
    """Deserialize a JSON array stored in the DB (``env_vars`` and friends).

    Returns ``None`` for empty / null / unparseable input. Accepts strings
    (raw JSON), already-materialized lists of dicts, and lists of Pydantic
    models (Prisma may hydrate a JSON column such as ``env_vars`` into
    ``MCPEnvVar`` objects); model entries are normalized to plain dicts so
    downstream consumers expecting ``List[Dict[str, Any]]`` validate.
    """
    if data is None or data == "" or data == []:
        return None
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return None
        data = parsed
    if not isinstance(data, list):
        return None
    return [
        item.model_dump(mode="json") if hasattr(item, "model_dump") else item
        for item in data
    ]

