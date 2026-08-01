
def set_isdisjoint(set1: set[T], set2: set[T]) -> bool:
    if not isinstance(set2, Iterable):
        raise TypeError(f"'{type(set2)}' object is not iterable")

    for x in set1:
        for y in set2:
            if not isinstance(y, Hashable):
                raise TypeError(f"unhashable type: '{type(y)}'")
            if x == y:
                return False
    return True

