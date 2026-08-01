
def test_symmetric_difference(idx, sort):
    first = idx[1:]
    second = idx[:-1]
    answer = idx[[-1, 0]]
    result = first.symmetric_difference(second, sort=sort)

    if sort is None:
        answer = answer.sort_values()

    tm.assert_index_equal(result, answer)

    # GH 10149
    cases = [klass(second.values) for klass in [np.array, Series, list]]
    for case in cases:
        result = first.symmetric_difference(case, sort=sort)
        tm.assert_index_equal(result, answer)

    msg = "other must be a MultiIndex or a list of tuples"
    with pytest.raises(TypeError, match=msg):
        first.symmetric_difference([1, 2, 3], sort=sort)

