
def test_ismember_tuple_with_nans():
    # GH-41836
    values = np.empty(2, dtype=object)
    values[:] = [("a", float("nan")), ("b", 1)]
    comps = [("a", float("nan"))]

    result = isin(values, comps)
    expected = np.array([True, False], dtype=np.bool_)
    tm.assert_numpy_array_equal(result, expected)

