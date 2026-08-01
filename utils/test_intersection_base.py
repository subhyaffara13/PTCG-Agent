
def test_intersection_base(idx, sort, klass):
    first = idx[2::-1]  # first 3 elements reversed
    second = idx[:5]

    if klass is not MultiIndex:
        second = klass(second.values)

    intersect = first.intersection(second, sort=sort)
    if sort is None:
        expected = first.sort_values()
    else:
        expected = first
    tm.assert_index_equal(intersect, expected)

    msg = "other must be a MultiIndex or a list of tuples"
    with pytest.raises(TypeError, match=msg):
        first.intersection([1, 2, 3], sort=sort)

