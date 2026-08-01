
def test_zeros_without_shape():
    arr = ImmutableDenseNDimArray.zeros()
    assert arr == ImmutableDenseNDimArray(0)

