
def _namedtuple_flatten_with_keys(
    d: NamedTuple,
) -> tuple[list[tuple[KeyEntry, Any]], Context]:
    values, context = _namedtuple_flatten(d)
    # pyrefly: ignore [bad-return]
    return (
        [
            (GetAttrKey(field), v)
            for field, v in zip(context._fields, values, strict=True)
        ],
        context,
    )

