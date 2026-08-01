
def _indices_for_nelems(nelems):
    """Returns slices of length nelems, from start onwards, in direction sign."""

    if nelems == 0:
        return [size // 2]  # int index

    res = []
    for step in (1, 2):
        for sign in (-1, 1):
            start = size // 2 - nelems * step * sign // 2
            stop = start + nelems * step * sign
            res.append(slice(start, stop, step * sign))

    return res

