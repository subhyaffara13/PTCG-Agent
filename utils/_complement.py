
def _complement(items: Mapping[str, int], pool: Mapping[str, int]) -> dict[str, int]:
    """Pool minus items, floored at 0."""
    return {k: max(0, int(pool.get(k, 0)) - int(items.get(k, 0))) for k in _ITEM_KEYS}


def _complement(items: Mapping[str, int], pool: Mapping[str, int]) -> dict[str, int]:
    """Pool minus items, floored at 0."""
    return {k: max(0, int(pool.get(k, 0)) - int(items.get(k, 0))) for k in _ITEM_KEYS}

