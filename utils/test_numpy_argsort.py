
def test_numpy_argsort(idx):
    result = np.argsort(idx)
    expected = idx.argsort()
    tm.assert_numpy_array_equal(result, expected)

    # these are the only two types that perform
    # pandas compatibility input validation - the
    # rest already perform separate (or no) such
    # validation via their 'values' attribute as
    # defined in pandas.core.indexes/base.py - they
    # cannot be changed at the moment due to
    # backwards compatibility concerns
    if isinstance(type(idx), (CategoricalIndex, RangeIndex)):
        msg = "the 'axis' parameter is not supported"
        with pytest.raises(ValueError, match=msg):
            np.argsort(idx, axis=1)

        msg = "the 'kind' parameter is not supported"
        with pytest.raises(ValueError, match=msg):
            np.argsort(idx, kind="mergesort")

        msg = "the 'order' parameter is not supported"
        with pytest.raises(ValueError, match=msg):
            np.argsort(idx, order=("a", "b"))

