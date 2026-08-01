
def key_to_id(value: Any) -> list[Any]:
    return [id(k) if key_is_id(k) else k for k in value]

