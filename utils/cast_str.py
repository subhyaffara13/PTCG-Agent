
def cast_str(obj):
    """Cast an object as a string."""
    if isinstance(obj, bytes):
        # really this should never happened, it should
        # have been base64 encoded before.
        warnings.warn(
            "A notebook got bytes instead of likely base64 encoded values."
            "The content will likely be corrupted.",
            UserWarning,
            stacklevel=3,
        )
        return obj.decode("ascii", "replace")
    if not isinstance(obj, str):
        raise AssertionError
    return obj

