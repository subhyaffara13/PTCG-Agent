
def get_id(obj):
    if obj is None:
        return None
    if isinstance(obj, (int, str)):
        try:
            return int(obj)
        except (ValueError, TypeError):
            return None
    if isinstance(obj, dict):
        val = obj.get("id")
        if val is not None:
            try:
                return int(val)
            except (ValueError, TypeError):
                pass
    for attr in ("id", "card_id"):
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            if val is not None:
                try:
                    return int(val)
                except (ValueError, TypeError):
                    pass
    return None


def get_id(obj):
    if obj is None:
        return None
    if isinstance(obj, (int, str)):
        try:
            return int(obj)
        except (ValueError, TypeError):
            return None
    if isinstance(obj, dict):
        val = obj.get("id")
        if val is not None:
            try:
                return int(val)
            except (ValueError, TypeError):
                pass
    for attr in ("id", "card_id"):
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            if val is not None:
                try:
                    return int(val)
                except (ValueError, TypeError):
                    pass
    return None


def get_id(schema):
    """
    Originally ID was `id` and since v7 it's `$id`.
    """
    return schema.get('$id', schema.get('id', ''))

