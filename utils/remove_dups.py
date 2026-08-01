
def remove_dups(types: list[T]) -> list[T]:
    if len(types) <= 1:
        return types
    # Get unique elements in order of appearance
    all_types: set[T] = set()
    new_types: list[T] = []
    for t in types:
        if t not in all_types:
            new_types.append(t)
            all_types.add(t)
    return new_types

