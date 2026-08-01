
def _dict_flatten_with_keys(
    d: dict[Any, T],
) -> tuple[list[tuple[KeyEntry, T]], Context]:
    values, context = _dict_flatten(d)
    # pyrefly: ignore [bad-return]
    return [(MappingKey(k), v) for k, v in zip(context, values, strict=True)], context

