
def test_numpy_ufuncs_reductions(index, func):
    # TODO: overlap with tests.series.test_ufunc.test_reductions
    if len(index) == 0:
        pytest.skip("Test doesn't make sense for empty index.")

    if isinstance(index, CategoricalIndex) and index.dtype.ordered is False:
        with pytest.raises(TypeError, match="is not ordered for"):
            func.reduce(index)
        return
    else:
        result = func.reduce(index)

    if func is np.maximum:
        expected = index.max(skipna=False)
    else:
        expected = index.min(skipna=False)
        # TODO: do we have cases both with and without NAs?

    assert type(result) is type(expected)
    if isna(result):
        assert isna(expected)
    else:
        assert result == expected

