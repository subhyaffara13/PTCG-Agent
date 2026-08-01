
def _tuple_flatten_with_keys(
    d: tuple[T, ...],
) -> tuple[list[tuple[KeyEntry, T]], Context]:
    values, context = _tuple_flatten(d)
    # pyrefly: ignore [bad-return]
    return [(SequenceKey(i), v) for i, v in enumerate(values)], context

