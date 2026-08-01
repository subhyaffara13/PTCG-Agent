
def _deque_unflatten(values: Iterable[T], context: Context) -> deque[T]:
    return deque(values, maxlen=context)

