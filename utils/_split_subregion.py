
def _split_subregion(a, b, xp, split_at=None):
    """
    Given the coordinates of a region like a=[0, 0] and b=[1, 1], yield the coordinates
    of all subregions, which in this case would be::

        ([0, 0], [1/2, 1/2]),
        ([0, 1/2], [1/2, 1]),
        ([1/2, 0], [1, 1/2]),
        ([1/2, 1/2], [1, 1])
    """
    xp = array_namespace(a, b)

    if split_at is None:
        split_at = (a + b) / 2

    left = [xp.stack((a[i], split_at[i])) for i in range(a.shape[0])]
    right = [xp.stack((split_at[i], b[i])) for i in range(b.shape[0])]

    a_sub = _cartesian_product(left)
    b_sub = _cartesian_product(right)

    for i in range(a_sub.shape[0]):
        yield a_sub[i, ...], b_sub[i, ...]

