
def test_rebuild_immutable_arrays():
    sparr = ImmutableSparseNDimArray(range(10, 34), (2, 3, 4))
    densarr = ImmutableDenseNDimArray(range(10, 34), (2, 3, 4))

    assert sparr == sparr.func(*sparr.args)
    assert densarr == densarr.func(*densarr.args)

