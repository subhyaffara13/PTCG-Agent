
def _tuple_flatten(d: tuple[T, ...]) -> tuple[list[T], Context]:
    return list(d), None

