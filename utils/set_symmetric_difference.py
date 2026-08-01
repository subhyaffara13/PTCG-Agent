
def set_symmetric_difference(
    set1: Iterable[T],
    set2: Iterable[T],
    cls: type[Any] = set,
) -> Any:
    symmetric_difference_set: set[T] = set()
    for x in set1:
        if x not in set2:
            symmetric_difference_set.add(x)
    for x in set2:
        if x not in set1:
            symmetric_difference_set.add(x)
    return cls(symmetric_difference_set)

