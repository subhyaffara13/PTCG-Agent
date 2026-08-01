
def test_overlapping_assignments():
    # Test automatically generated assignments which overlap in memory.

    inds = _indices(ndims)

    for ind in inds:
        srcidx = tuple(a[0] for a in ind)
        dstidx = tuple(a[1] for a in ind)

        _check_assignment(srcidx, dstidx)

