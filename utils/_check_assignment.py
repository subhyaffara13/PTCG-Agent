
def _check_assignment(srcidx, dstidx):
    """Check assignment arr[dstidx] = arr[srcidx] works."""

    arr = np.arange(np.prod(shape)).reshape(shape)

    cpy = arr.copy()

    cpy[dstidx] = arr[srcidx]
    arr[dstidx] = arr[srcidx]

    assert_(np.all(arr == cpy),
            f'assigning arr[{dstidx}] = arr[{srcidx}]')

