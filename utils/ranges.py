from typing import Tuple

def ranges(ints: Iterable[int]) -> Iterator[Tuple[int, int]]:
    # Yield sorted, non-overlapping (min, max) ranges of consecutive integers
    sorted_ints = iter(sorted(set(ints)))
    try:
        start = end = next(sorted_ints)
    except StopIteration:
        return
    for v in sorted_ints:
        if v - 1 == end:
            end = v
        else:
            yield (start, end)
            start = end = v
    yield (start, end)

