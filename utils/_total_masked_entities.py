
def _total_masked_entities(value: object) -> int | None:
    """``masked_entity_count`` is a ``{entity_type: count}`` map — sum to a total."""
    if isinstance(value, Mapping):
        total = sum(v for v in value.values() if isinstance(v, int))
        return total or None
    return as_int(value)

