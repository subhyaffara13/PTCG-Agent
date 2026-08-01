
def reverse_enumerate(xs: list[T]) -> Iterator[tuple[int, T]]:
    index = len(xs) - 1
    for x in xs[::-1]:
        yield index, x
        index -= 1

