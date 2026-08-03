import math


def circular_shifts(iterable, steps=1):
    """Yield the circular shifts of *iterable*.

    >>> list(circular_shifts(range(4)))
    [(0, 1, 2, 3), (1, 2, 3, 0), (2, 3, 0, 1), (3, 0, 1, 2)]

    Set *steps* to the number of places to rotate to the left
    (or to the right if negative).  Defaults to 1.

    >>> list(circular_shifts(range(4), 2))
    [(0, 1, 2, 3), (2, 3, 0, 1)]

    >>> list(circular_shifts(range(4), -1))
    [(0, 1, 2, 3), (3, 0, 1, 2), (2, 3, 0, 1), (1, 2, 3, 0)]

    """
    buffer = deque(iterable)
    if steps == 0:
        raise ValueError('Steps should be a non-zero integer')

    buffer.rotate(steps)
    steps = -steps
    n = len(buffer)
    n //= math.gcd(n, steps)

    for _ in repeat(None, n):
        buffer.rotate(steps)
        yield tuple(buffer)

