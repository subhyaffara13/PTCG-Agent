
def _check_argument(param, options, value, prefix=False):
    """Raise if value for param is not in options."""
    if prefix and value is not None:
        failure = not any(value.startswith(p) for p in options if isinstance(p, str))
    else:
        failure = value not in options
    if failure:
        raise ValueError(
            f"The value for `{param}` must be one of {options}, "
            f"but {repr(value)} was passed."
        )
    return value

