
def test_intersection_non_object(idx, sort):
    other = Index(range(3), name="foo")

    result = idx.intersection(other, sort=sort)
    expected = MultiIndex(levels=idx.levels, codes=[[]] * idx.nlevels, names=None)
    tm.assert_index_equal(result, expected, exact=True)

    # if we pass a length-0 ndarray (i.e. no name, we retain our idx.name)
    result = idx.intersection(np.asarray(other)[:0], sort=sort)
    expected = MultiIndex(levels=idx.levels, codes=[[]] * idx.nlevels, names=idx.names)
    tm.assert_index_equal(result, expected, exact=True)

    msg = "other must be a MultiIndex or a list of tuples"
    with pytest.raises(TypeError, match=msg):
        # With non-zero length non-index, we try and fail to convert to tuples
        idx.intersection(np.asarray(other), sort=sort)

