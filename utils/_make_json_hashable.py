
def _make_json_hashable(value: JsonValue) -> _HashableJsonValue:
    if isinstance(value, dict):
        return tuple(sorted((k, _make_json_hashable(v)) for k, v in value.items()))
    elif isinstance(value, list):
        return tuple(_make_json_hashable(v) for v in value)
    else:
        return value

