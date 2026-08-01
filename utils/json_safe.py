
def json_safe(data: object) -> object:
    """Translates a mapping / sequence recursively in the same fashion
    as `pydantic` v2's `model_dump(mode="json")`.
    """
    if is_mapping(data):
        return {json_safe(key): json_safe(value) for key, value in data.items()}

    if is_iterable(data) and not isinstance(data, (str, bytes, bytearray)):
        return [json_safe(item) for item in data]

    if isinstance(data, (datetime, date)):
        return data.isoformat()

    return data

