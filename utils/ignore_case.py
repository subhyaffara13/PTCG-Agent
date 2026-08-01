
def ignore_case(value: V) -> V:
    """For use as a postprocessor for :func:`make_attrgetter`. Converts strings
    to lowercase and returns other types as-is."""
    if isinstance(value, str):
        return t.cast(V, value.lower())

    return value

