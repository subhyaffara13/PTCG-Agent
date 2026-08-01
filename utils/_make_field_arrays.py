
def _make_field_arrays(*fields) -> list[np.ndarray]:
    length = None
    for x in fields:
        if isinstance(x, (list, np.ndarray, ABCSeries)):
            if length is not None and len(x) != length:
                raise ValueError("Mismatched Period array lengths")
            if length is None:
                length = len(x)

    # error: Argument 2 to "repeat" has incompatible type "Optional[int]"; expected
    # "Union[Union[int, integer[Any]], Union[bool, bool_], ndarray, Sequence[Union[int,
    # integer[Any]]], Sequence[Union[bool, bool_]], Sequence[Sequence[Any]]]"
    return [
        (
            np.asarray(x)
            if isinstance(x, (np.ndarray, list, ABCSeries))
            else np.repeat(x, length)  # type: ignore[arg-type]
        )
        for x in fields
    ]

