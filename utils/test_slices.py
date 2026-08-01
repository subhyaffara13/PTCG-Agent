
def test_slices():
    md = ImmutableDenseNDimArray(range(10, 34), (2, 3, 4))

    assert md[:] == ImmutableDenseNDimArray(range(10, 34), (2, 3, 4))
    assert md[:, :, 0].tomatrix() == Matrix([[10, 14, 18], [22, 26, 30]])
    assert md[0, 1:2, :].tomatrix() == Matrix([[14, 15, 16, 17]])
    assert md[0, 1:3, :].tomatrix() == Matrix([[14, 15, 16, 17], [18, 19, 20, 21]])
    assert md[:, :, :] == md

    sd = ImmutableSparseNDimArray(range(10, 34), (2, 3, 4))
    assert sd == ImmutableSparseNDimArray(md)

    assert sd[:] == ImmutableSparseNDimArray(range(10, 34), (2, 3, 4))
    assert sd[:, :, 0].tomatrix() == Matrix([[10, 14, 18], [22, 26, 30]])
    assert sd[0, 1:2, :].tomatrix() == Matrix([[14, 15, 16, 17]])
    assert sd[0, 1:3, :].tomatrix() == Matrix([[14, 15, 16, 17], [18, 19, 20, 21]])
    assert sd[:, :, :] == sd


def test_slices():
    md = MutableDenseNDimArray(range(10, 34), (2, 3, 4))

    assert md[:] == MutableDenseNDimArray(range(10, 34), (2, 3, 4))
    assert md[:, :, 0].tomatrix() == Matrix([[10, 14, 18], [22, 26, 30]])
    assert md[0, 1:2, :].tomatrix() == Matrix([[14, 15, 16, 17]])
    assert md[0, 1:3, :].tomatrix() == Matrix([[14, 15, 16, 17], [18, 19, 20, 21]])
    assert md[:, :, :] == md

    sd = MutableSparseNDimArray(range(10, 34), (2, 3, 4))
    assert sd == MutableSparseNDimArray(md)

    assert sd[:] == MutableSparseNDimArray(range(10, 34), (2, 3, 4))
    assert sd[:, :, 0].tomatrix() == Matrix([[10, 14, 18], [22, 26, 30]])
    assert sd[0, 1:2, :].tomatrix() == Matrix([[14, 15, 16, 17]])
    assert sd[0, 1:3, :].tomatrix() == Matrix([[14, 15, 16, 17], [18, 19, 20, 21]])
    assert sd[:, :, :] == sd


def test_slices(slice_test_df, slice_test_grouped):
    # Test tuple of slices
    result = slice_test_grouped._positional_selector[:2, -2:]
    expected = slice_test_df.iloc[[0, 1, 2, 3, 4, 6, 7]]

    tm.assert_frame_equal(result, expected)

