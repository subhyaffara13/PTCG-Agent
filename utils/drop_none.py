
def drop_none(values: Mapping[str, AttrValue | None]) -> AttributeMap:
    """Return ``values`` with ``None``-valued entries removed."""
    return {k: v for k, v in values.items() if v is not None}

