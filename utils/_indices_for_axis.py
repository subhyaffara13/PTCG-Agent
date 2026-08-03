import itertools

def _indices_for_axis():
    """Returns (src, dst) pairs of indices."""

    res = []
    for nelems in (0, 2, 3):
        ind = _indices_for_nelems(nelems)
        res.extend(itertools.product(ind, ind))  # all assignments of size "nelems"

    return res

