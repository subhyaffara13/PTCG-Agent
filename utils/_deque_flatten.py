
def _deque_flatten(d: deque[T]) -> tuple[list[T], Context]:
    return list(d), d.maxlen

