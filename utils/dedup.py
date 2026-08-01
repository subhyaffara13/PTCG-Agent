
def dedup(old: list[T]) -> list[T]:
    new: list[T] = []
    for x in old:
        if x not in new:
            new.append(x)
    return new

