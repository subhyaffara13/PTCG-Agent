
def _list_flatten_with_keys(d: list[T]) -> tuple[list[tuple[KeyEntry, T]], Context]:
    values, context = _list_flatten(d)
    # pyrefly: ignore [bad-return]
    return [(SequenceKey(i), v) for i, v in enumerate(values)], context

