
def test_searchsorted(request, index_or_series_obj):
    # numpy.searchsorted calls obj.searchsorted under the hood.
    # See gh-12238
    obj = index_or_series_obj

    if isinstance(obj, pd.MultiIndex):
        # See gh-14833
        request.applymarker(
            pytest.mark.xfail(
                reason="np.searchsorted doesn't work on pd.MultiIndex: GH 14833"
            )
        )
    elif obj.dtype.kind == "c" and isinstance(obj, Index):
        # TODO: Should Series cases also raise? Looks like they use numpy
        #  comparison semantics https://github.com/numpy/numpy/issues/15981
        mark = pytest.mark.xfail(reason="complex objects are not comparable")
        request.applymarker(mark)

    max_obj = max(obj, default=0)
    index = np.searchsorted(obj, max_obj)
    assert 0 <= index <= len(obj)

    index = np.searchsorted(obj, max_obj, sorter=range(len(obj)))
    assert 0 <= index <= len(obj)


def test_searchsorted(side, value):
    ri = RangeIndex(-3, 3, 2)
    result = ri.searchsorted(value=value, side=side)
    expected = Index(list(ri)).searchsorted(value=value, side=side)
    if isinstance(value, int):
        assert result == expected
    else:
        tm.assert_numpy_array_equal(result, expected)

