
def test_shape_of_invalid_index():
    # Pre-2.0, it was possible to create "invalid" index objects backed by
    # a multi-dimensional array (see https://github.com/pandas-dev/pandas/issues/27125
    # about this). However, as long as this is not solved in general,this test ensures
    # that the returned shape is consistent with this underlying array for
    # compat with matplotlib (see https://github.com/pandas-dev/pandas/issues/27775)
    idx = Index([0, 1, 2, 3])
    with pytest.raises(ValueError, match="Multi-dimensional indexing"):
        # GH#30588 multi-dimensional indexing deprecated
        idx[:, None]

