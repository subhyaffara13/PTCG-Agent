
def ndindex(*x: int) -> Generator[tuple[int, ...]]:
    """
    Generate all N-dimensional indices for a given array shape.

    Given the shape of an array, an ndindex instance iterates over the N-dimensional
    index of the array. At each iteration a tuple of indices is returned, the last
    dimension is iterated over first.

    This has an identical API to numpy.ndindex.

    Parameters
    ----------
    *x : int
        The shape of the array.
    """
    if not x:
        yield ()
        return
    for i in ndindex(*x[:-1]):
        for j in range(x[-1]):
            yield *i, j

