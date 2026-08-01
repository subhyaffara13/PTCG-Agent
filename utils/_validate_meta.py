
def _validate_meta(meta: str | list[str | list[str]] | None) -> None:
    """
    Validate that meta parameter contains only strings or lists of strings.
    Parameters
    ----------
    meta : str or list of str or list of list of str or None
        The meta parameter to validate.
    Raises
    ------
    TypeError
        If meta contains elements that are not strings or lists of strings.
    """
    if meta is None:
        return
    if isinstance(meta, str):
        return
    for item in meta:
        if isinstance(item, list):
            for subitem in item:
                if not isinstance(subitem, str):
                    raise TypeError(
                        "All elements in nested meta paths must be strings. "
                        f"Found {type(subitem).__name__}: {subitem!r}"
                    )
        elif not isinstance(item, str):
            raise TypeError(
                "All elements in 'meta' must be strings or lists of strings. "
                f"Found {type(item).__name__}: {item!r}"
            )

