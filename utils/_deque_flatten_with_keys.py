
def _deque_flatten_with_keys(
    d: deque[T],
) -> tuple[list[tuple[KeyEntry, T]], Context]:
    values, context = _deque_flatten(d)
    # pyrefly: ignore [bad-return]
    return [(SequenceKey(i), v) for i, v in enumerate(values)], context

