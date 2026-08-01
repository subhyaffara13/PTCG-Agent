
def maybe_cast_str_impl(x):
    """Converts numba UnicodeCharSeq (numpy string scalar) -> unicode type (string).
    Is a no-op for other types."""
    if isinstance(x, types.UnicodeCharSeq):
        return lambda x: str(x)
    else:
        return lambda x: x

