
def set_update(set1: set[T], *others: Iterable[T]) -> set[T]:
    if len(others) == 0:
        return set1

    for set2 in others:
        for x in set2:
            if x not in set1:
                set1.add(x)

