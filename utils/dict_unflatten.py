
def dict_unflatten(
    metadata: tuple[list[_KT], list[_KT]],
    values: Iterable[_VT],
    /,
) -> dict[_KT, _VT]:
    original_keys, sorted_keys = metadata
    d = dict.fromkeys(original_keys)
    d.update(zip(sorted_keys, values, strict=True))
    return d  # type: ignore[return-value]

